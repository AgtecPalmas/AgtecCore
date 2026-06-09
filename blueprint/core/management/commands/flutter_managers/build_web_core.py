"""
Build para gerenciar a cópia do core do projeto Flutter Web

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
import shutil
from pathlib import Path

from core.management.commands.utils import Utils


class FlutterWebBuildProject:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = self.command.snippet_dir
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_web_project = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/"
        )
        self._django_dir = self.command.path_root

    def __override_project(self):
        """
        def para sobrescrever o projeto Flutter Web,
        mais especificamente a pasta core
        """

        try:
            # Verificando se o core já existe
            if Utils.check_dir(f"{self.flutter_web_dir}/lib/core") is False:
                Utils.show_message("Adicionando o core ao projeto flutter")
                shutil.copytree(
                    f"{self.flutter_web_project}/core", f"{self.flutter_web_dir}/lib/core"
                )
            
            # Verificando se o diretório de constantes já existe
            if Utils.check_dir(f"{self.flutter_web_dir}/lib/constants") is False:
                # Copiando o diretório de constantes
                Utils.show_message("Adicionando as constantes ao projeto flutter")
                shutil.copytree(
                    f"{self.flutter_web_project}/constants", f"{self.flutter_web_dir}/lib/constants"
                )

            # Verificando se o diretório de apps já existe
            if Utils.check_dir(f"{self.flutter_web_dir}/lib/apps") is False:
                # Copiando o diretório de apps
                Utils.show_message("Adicionando as apps padrões ao projeto")
                shutil.copytree(
                    f"{self.flutter_web_project}/apps", f"{self.flutter_web_dir}/lib/apps"
                )
            
            # Verificando se o diretório de assets já existe
            if Utils.check_dir(f"{self.flutter_web_dir}/assets") is False:
                # Copiando o diretório de assets
                Utils.show_message("Adicionando os assets ao projeto")
                shutil.copytree(
                    f"{self.flutter_web_project}/assets", f"{self.flutter_web_dir}/assets"
                )

        except Exception as error:
            Utils.show_error(f"Error in _override_project: {error}")

    def build(self):
        """
        def para construir o projeto Flutter Web
        """
        try:
            self.__override_project()
        except Exception as error:
            Utils.show_error(f"Error in build: {error}")
