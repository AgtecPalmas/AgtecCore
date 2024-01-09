import logging
import os
import re
import sys

from base.settings import IGNORED_APPS as IGNORED_APPS_BASE
from core.views.constants import IGNORED_APPS, IGNORED_MODELS
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rich import box, print
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from rich.text import Text

from .constants.fastapi import IGNORE_FIELDS


class Utils(object):
    class ProgressBar(Progress):
        """Utiliza a Progress do rich para mostrar uma barra de progresso no console"""

        def __init__(
            self,
            spinner: str = "bouncingBall",
            speed: float = 0.3,
            hide_when_finish: bool = True,
            *args,
            **kwargs,
        ):
            super().__init__(transient=hide_when_finish, *args, **kwargs)
            self.columns = [
                SpinnerColumn(spinner_name=spinner, speed=speed),
                "[progress.description]{task.description}",
                TaskProgressColumn(),
                BarColumn(),
                TimeRemainingColumn(),
            ]

    @staticmethod
    def check_ignore_field(field) -> bool:
        return field in IGNORE_FIELDS

    def show_error(
        self: str,
        emoji: str = "anger",
        border_color: str = "red",
        exit: bool = True,
    ):
        """Método para mostrar uma mensagem de error no console do python

        Arguments:
            self {str} -- String contendo a mensagem que será mostrada no console
            emoji {str} -- String contendo o emoji que será mostrado no início do console
            border_color {str} -- String contendo a cor da borda do painel
            exit {bool} -- Booleano para determinar se o processo deve ser finalizado ou não
        """
        __log = logging.getLogger("logger")
        __log.setLevel(logging.INFO)

        emoji = f":{emoji}: " if emoji else ""
        message = f"{emoji}{self}\n\nPor favor consulte a documentação\nhttps://github.com/AgtecPalmas/AgtecCore"

        print(
            Panel.fit(
                message,
                box=box.ASCII2,
                border_style=border_color,
            )
        )
        if exit:
            sys.exit()

    def show_message(
        self,
        emoji: str = "white_heavy_check_mark",
        title: bool = False,
        box_style: box = box.HEAVY_EDGE,
        border_color: str = "green",
    ):
        """Método para mostrar uma mensagem no console do python

        Arguments:
            message {str} -- String contendo a mensagem que será mostrada no console
            emoji {str} -- String contendo o emoji que será mostrado no início do console
            title {bool} -- Booleano para determinar se a mensagem será mostrada como título ou não
            box_style {box} -- Objeto contendo o estilo da borda do painel
            border_color {str} -- String contendo a cor da borda do painel
        """
        __log = logging.getLogger("logger")
        __log.setLevel(logging.INFO)
        try:
            emoji = f":{emoji}: " if emoji else ""
            if title:
                print(
                    Panel.fit(
                        f"{emoji}{self}", box=box_style, border_style=border_color
                    )
                )
            else:
                print(emoji, self)
        except Exception as error:
            logging.error(error)

    @staticmethod
    def show_core_box(texto: str, tipo: str):
        """Método para mostrar uma mensagem no console do python

        Arguments:
            texto {str} -- String contendo a mensagem que será mostrada no console
            tipo {str} -- String contendo o tipo da mensagem que será mostrada no console
        """
        if tipo == "core":
            print(
                Panel(
                    Text("AGTEC CORE", justify="center", style="cyan bold"),
                    border_style="cyan",
                )
            )

        else:
            modelos = {
                "model": {
                    "emoji": "toolbox",
                    "box_style": box.HEAVY_EDGE,
                },
                "app": {
                    "emoji": "hourglass_flowing_sand",
                    "box_style": box.ASCII2,
                },
            }

            Utils.show_message(
                texto,
                emoji=modelos[tipo]["emoji"],
                title=True,
                box_style=modelos[tipo]["box_style"],
            )

    @staticmethod
    def contain_number(text: str) -> bool:
        try:
            return any(character.isdigit() for character in text)
        except Exception as error:
            Utils.show_error(f"Error in __contain_number: {error}")
            return False

    @staticmethod
    def get_verbose_name(apps, app_name: str = None, model_name: str = None) -> str:
        try:
            if app_name is not None:
                if model_name is not None:
                    _model = ContentType.objects.get(
                        app_label=app_name.lower(), model=model_name.lower()
                    )
                    return _model.model_class()._meta.verbose_name.title()
                __app_config = apps.get_app_config(app_name.lower())
                return __app_config.verbose_name.title() or app_name
        except Exception as error:
            if "ContentType matching query does not exist" not in str(error):
                Utils.show_message(f"Error in Utils.get_verbose_name: {error}")
            return model_name.title() or app_name.title()

    @staticmethod
    def check_dir(path: str) -> bool:
        """Método para verificar se o diretório passado como parâmetro existe

        Arguments:
            path {str} -- Caminho do diretório

        Returns:
            bool -- True se o diretório existir e False caso contrário.
        """
        __process_result = False
        try:
            __process_result = os.path.isdir(path)
        except Exception as error:
            Utils.show_error(f"Error in Utils.check_dir: {error}")
        finally:
            return __process_result

    @staticmethod
    def check_file(path: str) -> bool:
        """Método para verificar se o arquivo existe no caminho passado como parâmetro

        Arguments:
            path {str} - Caminho do arquivo

        Returns:
            bool - True se o arquivo existir e False caso contrário
        """
        __process_result = False
        try:
            __process_result = os.path.isfile(path)
        except Exception as error:
            Utils.show_error(f"Error in Utils.check_file: {error}")
        finally:
            return __process_result

    @staticmethod
    def check_content(path: str, text: str, use_regex: bool = False) -> bool:
        """Método para verificar se o conteúdo do parâmetro

        Arguments:
            path {str} - Caminho do arquivo
            text {str} - Texto para ser verificado se existe no conteúdo do arquivo passado no path

        Returns:
            bool - True se o conteúdo existir no arquivo e False caso contrário
        """
        __process_result = False
        try:
            if Utils.check_file(path):
                with open(path) as content_file:
                    content = content_file.read()
                    if use_regex:
                        pattern = f"\b{text}\b"
                        __process_result = re.search(pattern, content) is not None
                    else:
                        __process_result = text in content
        except Exception as error:
            Utils.show_error(f"Error in Utils.check_content: {error}")
        finally:
            return __process_result

    @staticmethod
    def check_file_is_locked(path: str) -> bool:
        """Método para verificar se no arquivo passado como parâmetro existe a palavra FileLocked
           caso existe o processo de parser do arquivo não será executado

        Arguments:
            path {str} - Caminho para o arquivo a ser analizado

        Returns:
            bool - True se a palavra existir e False caso contrário
        """
        __process_result = False
        try:
            if Utils.check_file(path):
                with open(path, encoding="utf-8") as file:
                    content = file.read()
                    __process_result = "#FileLocked" in content
        except Exception as error:
            Utils.show_error(f"Error in Utils.check_file: {error}")
        finally:
            if __process_result:
                path = path.split("\\")[-1]
                Utils.show_message(f"Arquivo [cyan]{path}[/] bloqueado", emoji="lock")
            return __process_result

    @staticmethod
    def get_snippet(path: str) -> str:
        """Método para retornar o conteúdo do arquivo a ser utilizado como modelos para gerar o
           arquivo baseado no models, gerando os arquivos de templates, views, urls, serializers,
           forms e também os arquivos do projeto Flutter.

        Arguments:
            path {str} - Caminho para o arquivo que serve como base para criar os arquivos do projeto

        Returns:
            str -- Texto do snippet para ser parseado e depois gerar o arquivo do projeto Django/Flutter
        """
        __content = ""
        try:
            if Utils.check_file(path):
                with open(path, "r", encoding="utf-8") as file:
                    __content = file.read()
        except Exception as error:
            Utils.show_error(f"Error in Utils.check_file: {error}")
        finally:
            return __content

    @staticmethod
    def create_directory(path: str, init: bool = False) -> bool:
        """Crie um diretório no caminho passado como parâmetro"""
        __process_result = False
        if not Utils.check_dir(path):
            try:
                os.makedirs(path)
                if init:
                    Utils.create_file(f"{path}/__init__.py")
                __process_result = True
            except Exception as error:
                Utils.show_error(f"Error in Utils.create_directory: {error}")
        return __process_result

    @staticmethod
    def create_file(path: str) -> bool:
        """Crie um arquivo no caminho passado como parâmetro"""
        if not Utils.check_file(path):
            with open(path, "w", encoding="utf-8") as arquivo:
                arquivo.write("")
            return True
        return False

    @staticmethod
    def replace_content(content: str, model: str, app: str, model_lower: str) -> str:
        """Substitui o conteúdo do snippet"""
        content = content.replace("$ModelClass$", model)
        content = content.replace("$app_name$", app)
        content = content.replace("$model_name$", model_lower)
        return content.replace("$App_Class$", app.title())

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Escreve o conteúdo em um arquivo"""
        with open(path, "w", encoding="utf-8") as arquivo:
            arquivo.write(content)
        return

    @staticmethod
    def append_file(path: str, content: str) -> None:
        """Escreve o conteúdo em um arquivo"""
        with open(path, "a", encoding="utf-8") as arquivo:
            arquivo.write(content)
        return

    @staticmethod
    def read_file(path: str) -> str:
        """Lê o conteúdo de um arquivo"""
        with open(path, "r", encoding="utf-8") as arquivo:
            return arquivo.readlines()

    @staticmethod
    def get_item_from_imports(content: str, search: str) -> list:
        """Retorna os itens importados de um arquivo"""
        content: list = content.replace("(", "").replace(")", "").split("from ")
        items: list = []

        for line in content:
            if f"{search} import" in line:
                line = line.split("import ")[1]
                items.extend(
                    item.strip() for item in line.split(",") if "AppIndex" not in item
                )
        return items

    @staticmethod
    def clear_string(string: str) -> str:
        """Remove todos os caracteres que não são letras ou underline"""
        return re.sub(r"[^a-zA-Z_]", "", string)

    @staticmethod
    def get_apps():
        # itens = {app:[models]}
        itens = {}

        for app in apps.get_app_configs():
            if app.name in IGNORED_APPS or app.name in IGNORED_APPS_BASE:
                continue

            itens[app.name] = []
            for model in app.get_models():
                if model._meta.model_name not in IGNORED_MODELS:
                    itens[app.name].append(model.__name__)

        return itens
