"""
Build para gerenciar a criação dos arquivos da camanda de models
de cada model da App, que serão criados dentro do diretório
models

"""
from pathlib import Path

from django.utils.text import slugify

from core.management.commands.utils import Utils


class AppsMobilePagesBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.flutter_web_dir = self.command.flutter_dir
        # TODO Refatorar os templates depois que tudo estiver funcionando.
        self.flutter_list_page_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_mobile_project/layers/listpage.txt"
        )
        self.flutter_content_page_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_mobile_project/layers/contentpage.txt"
        )

    def build(self):
        try:
            # Pegando os models da app
            self._models_app = self.app.get_models()

            for model in self._models_app:
                _model_app = self.app.name
                _model_app_lower = _model_app.lower()
                _model_name = model.__name__
                _model_name_lower = _model_name.lower()
                _app_file = Path(
                    f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/pages/{_model_name_lower}.list.dart"
                )
                # Parseando o snippet
                _content = Utils.get_snippet(self.flutter_list_page_snippet)
                _content = _content.replace("$ModelClass$", _model_name)
                # Gerando a String slug do models para usar na uri
                _model_name_slug = slugify(_model_name_lower)

                _content = _content.replace("$Model$", _model_name_slug)

                # Criando o arquivo de cada camada da app/models
                Utils.show_message(f"Criando {_app_file}")
                with open(_app_file, "w") as arquivo:
                    arquivo.write(_content)
                
                # Renderizando a página de conteúdo
                _app_file = Path(
                    f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/pages/{_model_name_lower}.content.dart"
                )
                # Parseando o snippet
                _content = Utils.get_snippet(self.flutter_content_page_snippet)
                _content = _content.replace("$ModelClass$", model.__name__)
                # Gerando a String slug do models para usar na uri
                _model_name_slug = slugify(_model_name_lower)

                _content = _content.replace("$Model$", _model_name_slug)

                # Criando o arquivo de cada camada da app/models
                Utils.show_message(f"Criando {_app_file}")
                with open(_app_file, "w") as arquivo:
                    arquivo.write(_content)


        except Exception as error:
            Utils.show_error(f"Error building models: {error}")
            raise error

