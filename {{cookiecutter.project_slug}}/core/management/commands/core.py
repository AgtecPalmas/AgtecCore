import contextlib

import requests
from decouple import config
from django.apps import apps
from django.core.management.base import BaseCommand

from core.management.commands.utils import Utils


def sanitize(version: str) -> list[int]:
    """Sanitizes a software version"""
    # 4 parts: django, major, minor, patch
    version = version.replace("v", "")
    version_parts = version.split(".")
    num_parts = len(version_parts)

    if num_parts < 4:
        version_parts += ["0"] * (4 - num_parts)

    return [int(part) for part in version_parts]


def compare_version(version1: str, version2: str) -> str:
    """Compara a primeira versão com a segunda versão"""

    version1 = sanitize(version1)
    version2 = sanitize(version2)

    for index in range(1, 4):
        if version1[index] > version2[index]:
            return "lower"

        elif version2[index] > version1[index]:
            return "higher"

    return "equal"


class Command(BaseCommand):
    help = "Exibe informações sobre o Core"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url: str = None
        self.token: str = None

        with contextlib.suppress(Exception):
            self.url = config("GITLAB_API_CORE_URL")
            self.token = config("GITLAB_TOKEN")

        self.last_version: str = None
        self.current_version: str = getattr(
            apps.get_app_config("core"), "version", "0.0.0.0"
        )
        self.django_version: int = int(self.current_version.split(".")[0][-1])
        self.last_django_version: int = 0

    def __remove_parser_arguments(self, parser) -> None:
        """Remove os argumentos padrões do Django causando conflito"""
        flags = ["--version", "--help", "-v", "-h"]

        for flag in flags:
            parser._optionals._option_string_actions.pop(flag)

    def add_arguments(self, parser) -> None:
        """Adiciona os argumentos para o comando"""
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

    def __validate_url_and_token(self) -> bool:
        """Valida a URL e o Token do GitLab"""
        if not self.url or not self.token:
            Utils.show_error(
                "URL do GitLab ou Token não foram definidos no arquivo .env"
            )
        elif "__id_projeto__" in self.url or "__url_gitlab__" in self.url:
            Utils.show_error(
                "URL do GitLab ou ID do projeto estão incorretos no arquivo .env"
            )
        else:
            return True

    def __get_tags_from_gitlab(self) -> str:
        """Retorna a última tag do projeto no GitLab"""
        if not self.__validate_url_and_token():
            return

        try:
            response = requests.get(
                url=f"{self.url}tags", headers={"Private-Token": self.token}
            )

            if response.status_code != 200:
                Utils.show_error(
                    f"Erro ao tentar obter a última tag do projeto no GitLab\n\
                        [red b]Status Code: {response.status_code}[/]"
                )

            tags = response.json()

            for tag in tags:
                tag_version = sanitize(tag.get("name"))
                if tag_version[0] > self.last_django_version:
                    self.last_django_version = tag_version[0]

            for tag in tags:
                tag_version = sanitize(tag.get("name"))
                if tag_version[0] == self.django_version:
                    self.last_version = tag.get("name")
                    return

            Utils.show_error(
                f"Seu Core aponta a versão {self.current_version}\
                \nMas não há registro do Core com a versão {self.django_version} do Django"
            )

        except requests.exceptions.RequestException as error:
            Utils.show_error(
                f"Erro ao tentar obter a última tag do projeto no GitLab\n{error}"
            )

    def __check_django_upgrade(self) -> None:
        """Verifica se o Django foi atualizado"""
        if self.django_version < self.last_django_version:
            Utils.show_message(
                title=True,
                emoji="rocket",
                self=f"Encontramos uma nova versão do Django: [green b]{self.last_django_version}[/]\
                    \nÉ recomendado que você atualize o Core e o Django",
            )

    def __check_update(self) -> None:
        """Verifica se existe uma nova versão do Core"""
        state: str = compare_version(self.last_version, self.current_version)

        if state == "lower":
            Utils.show_message(
                f"[green b]Atualização {self.last_version} disponível[/]\nVersão [cyan b]{self.current_version}[/] está sendo usada",
                emoji="up",
            )

        elif state == "higher":
            Utils.show_message(
                f"Algo está errado\nCore [green b]{self.last_version}[/]\nProjeto [red b]{self.current_version}[/]",
                emoji="rotating_light",
            )

        else:
            Utils.show_message(
                f"Você está na versão mais recente do Core: [green b]{self.current_version}[/]"
            )

    def __help(self) -> None:
        """Exibe a ajuda do comando"""
        Utils.show_message(
            f"[green b]AGTEC CORE[/] [cyan b]{self.current_version}[/]\
            \n\n[yellow b]Comandos[/]\
            \n[green b]--checkupdate[/] - Verifica se existe uma nova versão do Core\
            \n[green b]--help[/] ou [green b]-h[/] - Exibe esta mensagem\
            \n[green b]--version[/] ou [green b]-v[/] - Exibe a versão do Core",
            title=True,
            emoji="rocket",
        )

    def handle(self, *args, **options) -> None:
        """Executa o comando"""

        if options["version"]:
            Utils.show_message(f"Versão do Core: [green b]{self.current_version}[/]")

        elif options["checkupdate"]:
            self.__get_tags_from_gitlab()
            self.__check_django_upgrade()
            self.__check_update()

        else:
            self.__help()
