"""
Build para gerenciar a cópia do core do projeto Flutter Web

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
from pathlib import Path

from django.utils.text import slugify

from core.management.commands.utils import Utils


class AppsWebCubitStateManagerBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_state_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/layers/state.txt"
        )
        self.flutter_controller_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/layers/controller.txt"
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
                # Parseando o snippet
                _content = Utils.get_snippet(self.flutter_state_snippet)
                _content = _content.replace("$ModelClass$", _model_name)
                _content = _content.replace(
                    "$ModelClassCamelCase$", _model_name_lower
                )
                # Gerando a String slug do models para usar na uri
                _model_name_slug = slugify(_model_name_lower)

                _content = _content.replace("$Model$", _model_name_slug)
                _content = _content.replace("$App$", _model_app_lower)

                # Criando o state do gerenciador de estado Cubit
                _state_file = Path(f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/states/{_model_name_lower}.dart")
                Utils.show_message(
                    f"Criando {_state_file}"
                )
                with open(_state_file, "w") as arquivo:
                    arquivo.write(_content)
                
                # Parseando o snippet
                _content_controller = Utils.get_snippet(self.flutter_controller_snippet)
                _content_controller = _content_controller.replace("$ModelClass$", _model_name)
                _content_controller = _content_controller.replace(
                    "$ModelClassCamelCase$", _model_name_lower
                )
                # Gerando a String slug do models para usar na uri
                _model_name_slug = slugify(_model_name_lower)

                _content_controller = _content_controller.replace("$Model$", _model_name_slug)
                _content_controller = _content_controller.replace("$App$", _model_app_lower)

                # Criando o controller do gerenciador de estado Cubit
                _controller_file = Path(f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/controllers/{_model_name_lower}.dart")
                Utils.show_message(
                    f"Criando {_controller_file}"
                )
                with open(_controller_file, "w") as arquivo:
                    arquivo.write(_content_controller)
                

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsWebDirectoriesBuilder: {error}"
            )
            return
