"""
Build para gerenciar a cópia do core do projeto Flutter Web

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
from pathlib import Path

from django.utils.text import slugify

from core.management.commands.utils import Utils


class AppsWebRouterBuilder:
    def __init__(self, command, app, model=None) -> None:
        self.command = command
        self.app = app
        self.model = model
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_service_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/layers/router.txt"
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
                _app_file = Path(f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/routes/{_model_name_lower}.dart")

                if self.model is not None and _model_name_lower != self.model.lower():
                    continue

                # Verificando se o arquivo já existe e está bloqueado
                if Utils.check_file_is_locked(str(_app_file)):
                    return

                # Parseando o snippet
                _content = Utils.get_snippet(self.flutter_service_snippet)
                _content = _content.replace("$ModelClass$", _model_name)
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
                f"Erro ao executar o build de AppsWebDirectoriesBuilder: {error}"
            )
            return
