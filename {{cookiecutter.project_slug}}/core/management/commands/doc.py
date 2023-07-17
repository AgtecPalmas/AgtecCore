import os
import subprocess
from django.apps import apps
from django.core.management.base import BaseCommand
from core.management.commands.utils import Utils
from base.settings import DOC_APPS


class Command(BaseCommand):
    help = (
        """Manager responsible for generating documentation for the development team"""
    )

    def __init__(self):
        super().__init__()
        self.projeto = None
        self.desenvolvedor = None
        self.path_root = os.getcwd()
        self.__docs_path = f"{self.path_root}/doc"

    def add_arguments(self, parser):
        parser.add_argument("projeto", type=str)
        parser.add_argument("desenvolvedor", type=str)

    @staticmethod
    def __title(string) -> str:
        try:
            string = string.replace("_", " ").title()
        finally:
            return string

    def __parser_documentation(self):
        apps_instaladas = self.verificar_apps_instaladas()
        self.path_core = os.path.join(self.path_root, "core")
        try:
            content = Utils.get_snippet(
                os.path.join(
                    self.path_core, "management/commands/snippets/sphinx_doc/config.txt"
                )
            )
            content = content.replace("$project$", "base")
            content = content.replace("$Project$", self.__title(self.projeto))
            content = content.replace("$Desenvolvedor$", self.desenvolvedor)

            with open(f"{self.__docs_path}/source/conf.py", "w") as arquivo:
                arquivo.write(content)
        except:
            pass

        try:
            __make_content = Utils.get_snippet(
                os.path.join(
                    self.path_core, "management/commands/snippets/sphinx_doc/make.txt"
                )
            )

            with open(f"{self.__docs_path}/Makefile", "w") as arquivo:
                arquivo.write(__make_content)
        except:
            pass
        try:
            __make_content = Utils.get_snippet(
                os.path.join(
                    self.path_core, "management/commands/snippets/sphinx_doc/make.txt"
                )
            )

            with open(f"{self.__docs_path}/Makefile", "w") as arquivo:
                arquivo.write(__make_content)
        except:
            pass
        try:
            __make_bat_content = Utils.get_snippet(
                os.path.join(
                    self.path_core,
                    "management/commands/snippets/sphinx_doc/make_bat.txt",
                )
            )

            with open(f"{self.__docs_path}/make.bat", "w") as arquivo:
                arquivo.write(__make_bat_content)
        except:
            pass
        try:
            __modules_content = Utils.get_snippet(
                os.path.join(
                    self.path_core,
                    "management/commands/snippets/sphinx_doc/modules.txt",
                )
            )

            __module_apps = ""
            for __app in apps_instaladas:
                __module_apps += f"   {__app}\n"

            __modules_content = __modules_content.replace(
                "$App$", self.__title(self.projeto)
            )
            __modules_content = __modules_content.replace("$Modules$", __module_apps)

            with open(f"{self.__docs_path}/source/modules.rst", "w") as arquivo:
                arquivo.write(__modules_content)

            __rst_content = Utils.get_snippet(
                os.path.join(
                    self.path_core,
                    "management/commands/snippets/sphinx_doc/index_rst.txt",
                )
            )

            with open(f"{self.__docs_path}/source/index.rst", "w") as arquivo:
                arquivo.write(__rst_content)
        except:
            pass
        try:
            for app in apps_instaladas:
                __content = Utils.get_snippet(
                    os.path.join(
                        self.path_core,
                        "management/commands/snippets/sphinx_doc/rst.txt",
                    )
                )
                content = content.replace("$App$", app.title())
                content = content.replace("$app$", app)
                arquivo_rst = f"{self.__docs_path}/source/{app.lower()}.rst"

                with open(
                        arquivo_rst, "w"
                ) as arquivo:
                    arquivo.write(__content)

                self.build_rst(self, arquivo_rst, "views", app)
                self.build_rst(self, arquivo_rst, "api", app)

            subprocess.run(["sphinx-apidoc", "-f", "-o", "doc", "source"])
            subprocess.run(["sphinx-build", "-M", "html", "doc\source", "doc\source"])
        except:
            pass

    @staticmethod
    def build_rst(self, arquivo_rst, modulo, app):
        with open(arquivo_rst, "a") as arquivo:
            caminho_app = os.path.join(self.path_root, app)
            caminho_views = os.path.join(caminho_app, modulo)
            if os.path.isdir(caminho_views):
                arquivo.write(f"\n{modulo.capitalize()}")
                arquivo.write("\n-----------------------------")
                for arquivo_view in os.listdir(caminho_views):
                    if arquivo_view.endswith(".py"):
                        nome_modulo = os.path.splitext(arquivo_view)[0]
                        caminho_modulo = f"{app}.{modulo}.{nome_modulo}"
                        arquivo.write(f"\n\n.. automodule:: {caminho_modulo}\n")
                        arquivo.write("   :members:\n")

    @staticmethod
    def verificar_apps_instaladas():
        apps_instaladas = []

        for __app in DOC_APPS:
            if apps.is_installed(__app):
                apps_instaladas.append(__app)
            else:
                Utils.show_error(f"  A aplicação '{__app}' não está no INSTALLED_APPS do settings.", exit=False)

        return apps_instaladas

    @staticmethod
    def criar_diretorios(docs_path):
        directories = [
            docs_path,
            f"{docs_path}/build",
            f"{docs_path}/source",
            f"{docs_path}/source/_templates",
            f"{docs_path}/source/_static"
        ]

        for directory in directories:
            Utils.create_directory(directory)

    def handle(self, *args, **options):
        if not DOC_APPS:
            Utils.show_error(
                "É obrigatório a configuração no settings do projeto das DOC_APPS", exit=False
            )
            return

        self.projeto = options["projeto"]
        self.desenvolvedor = options["desenvolvedor"]
        __path = self.path_root

        self.criar_diretorios(self.__docs_path)
        self.__parser_documentation()
