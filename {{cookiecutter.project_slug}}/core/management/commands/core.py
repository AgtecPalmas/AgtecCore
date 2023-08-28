import contextlib
import re
from string import Template

import requests
from decouple import config
from django.apps import apps
from django.core.management.base import BaseCommand
from packaging.version import parse

from core.management.commands.utils import Utils

MESSAGES = {
    "erro_exception": Template(
        "Erro ao tentar obter tags do projeto no Github\n$exception"
    ),
    "erro_status_code": Template(
        "Erro ao tentar obter a última tag do projeto no Github\n[red b]Status Code: $status_code[/]"
    ),
    "erro_url_env": Template("URL do Github não foi definido no arquivo .env"),
    "error_version": Template(
        "Algo está errado\nCore $version_core\nProjeto $version_project"
    ),
    "help": Template(
        "[green b]AGTEC CORE[/] [cyan b]$version - $codename[/]\
            \n\n[yellow b]Comandos[/]\
            \n[green b]--checkupdate[/] - Verifica se existe uma nova versão do Core\
            \n[green b]--help[/] ou [green b]-h[/] - Exibe esta mensagem\
            \n[green b]--version[/] ou [green b]-v[/] - Exibe a versão do Core"
    ),
    "new_core_version": Template(
        "Atualização $version disponível\nVersão $current_version está sendo usada\n\nBaixar atualização\n$download_url"
    ),
    "new_django_version": Template(
        "Encontramos uma nova versão do Django: $version\nÉ recomendado que você atualize o Core e o Django"
    ),
    "not_found_core_version": Template(
        "Não encontramos versões do Core para o Django $version"
    ),
    "success_version": Template("Você está na versão mais recente do Core: $version"),
    "version": Template("Versão do Core: [green b]$version - $codename[/]"),
}


def get_tag_django_version(tag: str) -> int:
    """Returns the Django version of the tag"""
    return int(re.sub(r"[^0-9]", "", tag.split(".")[0]))


def compare_version(version1: str, version2: str) -> str:
    """Compare two versions"""
    if parse(version1) > parse(version2):
        return 1

    elif parse(version1) < parse(version2):
        return -1

    return 0


class Command(BaseCommand):
    help = "Exibe informações sobre o Core"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url_github: str = None

        with contextlib.suppress(Exception):
            self.url_github = config("GITHUB_API_CORE_URL")

        self.releases: list[dict] = []
        self.versions: dict[str, dict[str, str]] = {}

        self.core_project_version: str = getattr(
            apps.get_app_config("core"), "version", "0"
        )
        self.core_codename: str = getattr(
            apps.get_app_config("core"), "codename", "Null"
        )

        self.django_project_version: int = get_tag_django_version(
            self.core_project_version
        )
        self.django_last_version: int = 0

    def __remove_parser_arguments(self, parser) -> None:
        """Remove the default arguments from the parser"""
        flags = ["--version", "--help", "-v", "-h"]

        for flag in flags:
            parser._optionals._option_string_actions.pop(flag)

    def add_arguments(self, parser) -> None:
        """Add arguments to the parser"""
        self.__remove_parser_arguments(parser)

        parser.add_argument(
            "--version",
            "-v",
            action="store_true",
            dest="version",
            help="Exibe a versão do Core",
        )
        parser.add_argument(
            "--checkupdate",
            action="store_true",
            dest="checkupdate",
            help="Verifica se existe uma nova versão do Core",
        )
        parser.add_argument(
            "-h",
            "--help",
            action="store_true",
            dest="help",
            help="Exibe a ajuda do comando",
        )

    def __validate_env_variables(self) -> bool:
        """Valid if the url are defined"""
        if not self.url_github:
            Utils.show_error(MESSAGES["erro_url_env"].substitute())
            return False
        return True

    def __get_tags_from_github(self) -> None:
        """Returns the tags from Github"""
        if not self.__validate_env_variables():
            return

        try:
            response = requests.get(url=f"{self.url_github}/releases", timeout=5)

            if response.status_code != 200:
                Utils.show_error(
                    MESSAGES["erro_status_code"].substitute(
                        status_code=response.status_code
                    )
                )

            self.releases = response.json()

        except requests.exceptions.RequestException as error:
            Utils.show_error(MESSAGES["erro_exception"].substitute(exception=error))

    def __populate_versions(self) -> None:
        """Populate the versions"""
        for release in self.releases:
            tag_name: str = release.get("tag_name")
            tag_django_version = get_tag_django_version(tag_name)
            version_from_versions = self.versions.get(tag_django_version, {}).get(
                "tag_name", "0"
            )

            if tag_django_version > self.django_last_version:
                self.django_last_version = tag_django_version

            if compare_version(tag_name, version_from_versions) == 1:
                self.versions[tag_django_version] = {
                    "tag_name": tag_name,
                    "html_url": release.get("html_url"),
                }

    def __check_django_upgrade(self) -> None:
        """Check if the Django version is the last"""
        if self.django_project_version < self.django_last_version:
            Utils.show_message(
                title=True,
                emoji="rocket",
                self=MESSAGES["new_django_version"].substitute(
                    version=self.django_last_version,
                ),
            )

    def __check_core_version(self) -> bool:
        """Check if there is a version of the Core for the Django version"""
        if not self.versions.get(self.django_project_version):
            Utils.show_message(
                title=True,
                emoji="rocket",
                self=MESSAGES["not_found_core_version"].substitute(
                    version=self.django_project_version
                ),
            )
            return False
        return True

    def __check_core_update(self) -> None:
        """Check if the Core version is the last"""
        last_core_version_current_django: str = self.versions[
            self.django_project_version
        ]
        state: str = compare_version(
            self.core_project_version, last_core_version_current_django["tag_name"]
        )

        if state == -1:
            Utils.show_message(
                MESSAGES["new_core_version"].substitute(
                    version=last_core_version_current_django["tag_name"],
                    current_version=self.core_project_version,
                    download_url=last_core_version_current_django["html_url"],
                ),
                emoji="up",
            )

        elif state == 1:
            Utils.show_message(
                MESSAGES["error_version"].substitute(
                    version_core=last_core_version_current_django["tag_name"],
                    version_project=self.core_project_version,
                ),
                emoji="rotating_light",
            )

        else:
            Utils.show_message(
                MESSAGES["success_version"].substitute(
                    version=self.core_project_version
                )
            )

    def __help(self) -> None:
        """Show help message"""
        Utils.show_message(
            MESSAGES["help"].substitute(
                version=self.core_project_version, codename=self.core_codename
            ),
            title=True,
            emoji="rocket",
        )

    def handle(self, *args, **options) -> None:
        """Handle the command"""

        if options["version"]:
            Utils.show_message(
                MESSAGES["version"].substitute(
                    version=self.core_project_version, codename=self.core_codename
                ),
            )

        elif options["checkupdate"]:
            self.__get_tags_from_github()
            self.__populate_versions()
            self.__check_django_upgrade()

            if self.__check_core_version():
                self.__check_core_update()

        else:
            self.__help()
