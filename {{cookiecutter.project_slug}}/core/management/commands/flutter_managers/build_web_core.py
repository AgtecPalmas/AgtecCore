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
        self.snippet_web_dir = self.command.snippet_web_dir
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_web_project = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/"
        )
        self._django_dir = self.command.path_root

    def __create_base_project(self):
        """Método para criar o projeto Flutter Web
        que deverá ser criado como subdiretório do diretório FlutterWeb
        ficando o diretório pai no mesmo nível do Django e do Flutter"""

        try:
            if not Utils.check_dir(self.flutter_web_project):
                Utils.show_message("Criando projeto Flutter Web")

                _cmd = [
                    "flutter",
                    "create",
                    "--project-name",
                    f"{self.flutter_project.lower()}",
                    "--org",
                    f"{self.organization_flutter_name}",
                    "--platforms",
                    "web",
                    f"{self.flutter_web_project}",
                ]

                subprocess.call(
                    _cmd,
                    text=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                shutil.copyfile(
                    f"{self.snippet_dir}/README.md", f"{self.flutter_dir}/README.md"
                )
        except Exception as error:
            Utils.show_error(f"Error ao criar o projeto flutter web: {error}")

    def __override_project(self):
        """
        Método para sobrescrever o projeto Flutter Web,
        mais especificamente a pasta core
        """

        try:
            Utils.show_message(
                f"Substituindo o core do projeto Flutter Web: {self.flutter_web_dir}"
            )
            shutil.rmtree(f"{self.flutter_web_dir}/core")
            shutil.copytree(
                f"{self.flutter_web_project}/core", f"{self.flutter_web_dir}/core"
            )
        except Exception as error:
            Utils.show_error(f"Error in _override_project: {error}")

    def build(self):
        """
        Método para construir o projeto Flutter Web
        """
        try:
            self.__override_project()
        except Exception as error:
            Utils.show_error(f"Error in build: {error}")
