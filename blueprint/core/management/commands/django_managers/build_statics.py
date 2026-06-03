from pathlib import Path
import os

from ..utils import Utils


class StaticsBuild:
    def __init__(self, command):
        self.command = command

    def build(self):
        """Método responsável por criar a estrutura de diretórios static da app/models
        - APP
            - static
                - MODEL
                    - css
                    - js
        """
        try:
            if self.command.app is None:
                Utils.show_error("A app não foi informada", emoji="warning")
            if self.command.model is None:
                Utils.show_error("O model não foi informado", emoji="warning")

            # Criando o path para criação dos diretórios
            path = Path(f"{self.command.path_app}/static")

            # Verificando se o static da app já foi criado
            if Utils.check_dir(str(path)) is False:
                # Criando o diretório static da app
                os.mkdir(path)

            # Criando o diretório do models dentro do static criado na etapa anterior
            path = Path(f"{path}/{self.command.model_lower}")
            if Utils.check_dir(str(path)):
                Utils.show_message(
                    "O diretório [cyan]static[/] já existe",
                )
                return
            os.mkdir(path)
            Utils.show_message(
                "Diretório [cyan]static[/] criado com sucesso",
            )

            # Criando os subdiretórios css e js
            os.mkdir(Path(f"{path}/css"))

            # Criando o arquivo css
            path_css = Path(f"{path}/css/estilo.css")
            if Utils.check_file(str(path_css)) is False:
                with open(path_css, "w") as file:
                    file.write("/* CSS */")
            Utils.show_message(
                "Diretório static da app/models css criado com sucesso",
            )
            os.mkdir(Path(f"{path}/js"))

            # Criando o arquivo js
            path_js = Path(f"{path}/js/script.js")
            if Utils.check_file(str(path_js)) is False:
                with open(path_js, "w") as file:
                    file.write("/* JS */")
            Utils.show_message(
                "Diretório static da app/models js criado com sucesso",
            )

        except Exception as e:
            Utils.show_error(
                f"Erro ao criar os diretórios static da app/models: {e}",
            )
