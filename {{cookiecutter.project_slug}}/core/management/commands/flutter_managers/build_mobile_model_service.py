"""
Build para gerenciar a cópia do core do projeto Flutter Mobile

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
import re
from pathlib import Path

from django.utils.text import slugify

from core.management.commands.utils import Utils


class AppsMobileServiceBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.flutter_dir = self.command.flutter_dir
        self.fluttersnippet = Path(
            f"{self.command.path_command}/snippets/flutter_mobile_project/layers/service.txt"
        )

    def build(self):
        """
        build _summary_
        """
        try:
            self._models_app = self.app.get_models()
            for model in self._models_app:
                _model_app = self.app.name
                _model_app_lower = _model_app.lower()
                _model_name = model.__name__
                _model_name_lower = _model_name.lower()

                _app_file = Path(f"{self.flutter_dir}/lib/apps/{_model_app_lower}/services/{_model_name_lower}.dart")
                
                # Parseando o snippet
                _content = Utils.get_snippet(self.fluttersnippet)
                _content = _content.replace("$ModelClass$", _model_name)
                # Convertendo o _model_app para snake_case
                _content = _content.replace(
                    "$ModelSnakeCase$",
                    re.sub(r"(?<!^)(?=[A-Z])", "_", _model_name).lower(),
                )
                # Gerando a String slug do models para usar na uri
                _model_name_slug = slugify(_model_name_lower)

                _content = _content.replace("$Model$", _model_name_slug)
                _content = _content.replace("$App$", _model_app_lower)

                # Criando o arquivo de cada camada da app/models
                Utils.show_message(
                    f"Criando {_app_file}"
                )
                with open(_app_file, "w") as arquivo:
                    arquivo.write(_content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsMobileDirectoriesBuilder: {error}"
            )
            return
