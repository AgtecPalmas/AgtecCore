import contextlib
import os
import re
import shutil
import subprocess
import zipfile
from string import Template

import requests
from core.management.commands.utils import Utils
from decouple import config
from django.apps import apps
from django.core.management.base import BaseCommand
from packaging.version import parse

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
        "[green b]AGTEC CORE[/]\
            \n[cyan b]$version - $codename[/]\
            \n\n[yellow b]Comandos[/]\
            \n[green b]--upgrade[/]\tVerifica se existe uma nova versão do Core e atualiza\
            \n[green b]--help[/], [green b]-h[/]\tExibe esta mensagem\
            \n[green b]--version[/], [green b]-v[/]\tExibe a versão do Core"
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
    "cannot_upgrade": "Não podemos atualizar o Core\nFaça a atualização manualmente",
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
        self.versions: dict[str, dict[str, str, int]] = {}

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
        self.download_zip_name: str = "core.zip"

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
            "-h",
            "--help",
            action="store_true",
            dest="help",
            help="Exibe a ajuda do comando",
        )
        parser.add_argument(
            "--upgrade",
            action="store_true",
            dest="upgrade",
            help="Atualiza o Core para a última versão",
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
        """Populate the versions, one index per Django version"""
        """Example
        {
            "4": {
                "tag_name": "4.0.0",
                "html_url": "url"
                "id": release_id
                "zip": "zip_url"
                }
        }
        """

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
                    "id": release.get("id"),
                    "zip": release.get("zipball_url"),
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

    def __check_core_update(self) -> int:
        """Check if the Core version is the last

        Returns:
            1 if something is wrong

            -1 if there is a new version

            0 if the version is the same
        """

        if self.versions.get(self.django_project_version) is None:
            Utils.show_error(
                MESSAGES["not_found_core_version"].substitute(
                    version=self.django_project_version
                )
            )

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

        return state

    def __upgrade(self) -> None:
        """Upgrade the Core"""
        state: int = self.__check_core_update()

        if state != -1:
            return

        if input("Deseja atualizar o Core? [S/N]: ").lower() != "s":
            Utils.show_message("Operação cancelada")
            return

        release = self.versions[self.django_project_version]
        self.__download_update(release["zip"])
        self.__prepare_temp_folder()

        os.remove(self.download_zip_name)

        self.__upgrade_core()
        self.__upgrade_base()
        self.__upgrade_requirements()

        shutil.rmtree("temp")

        Utils.show_message("Core atualizado com sucesso")
        Utils.show_message(
            "Se você fez alguma alteração no core, verifique se não perdeu nada"
        )

    def __prepare_temp_folder(self) -> None:
        """Prepare the temp folder"""
        if os.path.exists("temp"):
            shutil.rmtree("temp")

        Utils.show_message("Extraindo arquivos")
        with zipfile.ZipFile(self.download_zip_name, "r") as zip_ref:
            zip_ref.extractall("temp")

        root_folder = os.listdir("temp")[0]

        for file in os.listdir(f"temp/{root_folder}/{{{{cookiecutter.project_slug}}}}"):
            shutil.move(
                f"temp/{root_folder}/{{{{cookiecutter.project_slug}}}}/{file}",
                "temp/",
            )

    def __download_update(self, zip_url: str) -> None:
        """Download the update"""
        Utils.show_message("Baixando atualização")
        download = requests.get(
            zip_url,
            timeout=10,
        )

        if download.status_code != 200:
            Utils.show_error(
                MESSAGES["erro_status_code"].substitute(
                    status_code=download.status_code
                )
            )

        with open(self.download_zip_name, "wb") as file:
            file.write(download.content)

    def __upgrade_core(self) -> None:
        """Compress the current core folder and move the new core folder"""

        Utils.show_message("Atualizando Core")
        try:
            shutil.make_archive("core_bkp", "zip", "core")
            shutil.rmtree("core")
            shutil.copytree(
                "temp/core",
                "core",
            )
        except Exception as error:
            Utils.show_error(
                f"Erro ao tentar excluir e mover o Core\n{error}",
                emoji="rotating_light",
            )

    def __upgrade_base(self) -> None:
        """Check if there are newer variables inside the base/settings file and upgrade it"""
        Utils.show_message("Atualizando base/settings.py")

        with open(
            "temp/base/settings.py",
            "r",
        ) as file:
            new_settings = file.read()

        with open("base/settings.py", "r") as file:
            current_settings = file.read()

        # Get variables UPPERCASE from the files
        new_settings_vars = re.findall(r"([A-Z_]+)\s*=", new_settings)
        current_settings_vars = re.findall(r"([A-Z_]+)\s*=", current_settings)

        if len(new_settings_vars) == len(current_settings_vars):
            Utils.show_message("Nenhuma variável nova encontrada")
            return

        for var in new_settings_vars:
            if var not in current_settings_vars:
                current_settings += f"\n{var} = None"
                Utils.show_message(
                    f"Nova variável encontrada: {var}, lembre de alterá-la"
                )

        with open("base/settings.py", "w") as file:
            file.write(current_settings)

    def __upgrade_requirements(self) -> None:
        """Upgrade the requirements file"""
        Utils.show_message("Atualizando requirements")

        files_in = [
            "requirements.in",
            "requirements-dev.in",
            "requirements-extras.in",
        ]
        files_txt = [
            "requirements.txt",
            "requirements-dev.txt",
            "requirements-extras.txt",
        ]

        for file in files_in + files_txt:
            with contextlib.suppress(FileNotFoundError):
                shutil.copy(f"temp/{file}", file)

        try:
            for file in files_in:
                subprocess.run(
                    f"pip-compile {file}",
                    shell=True,
                    check=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
        except Exception:
            Utils.show_error(
                "Erro ao tentar compilar os arquivos de requirements, faça 'pip-compile <arquivo>' manualmente",
                emoji="rotating_light",
            )

    def __update_command_object(self) -> None:
        """Update the Command Object to the current state"""
        self.__get_tags_from_github()
        self.__populate_versions()
        self.__check_django_upgrade()

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

        elif options["upgrade"]:
            self.__update_command_object()
            self.__upgrade()

        else:
            self.__help()
