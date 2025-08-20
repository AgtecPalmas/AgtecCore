"""
Build para gerenciar a cópia do core do projeto Flutter Web

Aqui será feita a copia pura, sem necessidade de mapear as classes
do projeto Django

"""
from pathlib import Path

from base.settings import FLUTTER_APPS_WEB
from core.management.commands.utils import Utils


class AppsWebInjectProvidersBuilder:
    def __init__(self, command, flutter_project) -> None:
        self.command = command
        self.flutter_project = flutter_project
        self.flutter_web_dir = self.command.flutter_dir

    def build(self):
        from core.management.commands.flutter import AppModel
        """
        Método para construir os registros dos providers
        para serem injetados no arquivo main.dart
        devendo ser gerado tanto os imports como os registros
        propriamente ditos.

        e.g. BlocProvider<UsuarioController>(create: (_) => UsuarioController()),
        """
        try:
            _list_controller_register = ""
            _list_controller_import = ""
            # Executando o looping pelas apps do flutter
            for app in FLUTTER_APPS_WEB:
                # Pegando a app
                _app = AppModel(self.flutter_project, app)
                # Percorrendo os models de cada app
                for model in _app.models:
                    if len(model) < 2:
                        continue
                    _title = model[1]
                    _model = model[2];
                    _comando = f"BlocProvider<{_title}Controller>(create: (_) => {_title}Controller()),\n"
                    _import = f"import 'apps/{app.lower()}/controllers/{_model}.dart';\n"
                    _list_controller_register += _comando
                    _list_controller_import += _import

            _routers_file = Path(f"{self.flutter_web_dir}/lib/main.dart")
            _routers_content = Utils.get_snippet(_routers_file)
            _routers_content = _routers_content.replace("$ImportMultiBlocProviders$", _list_controller_import)
            _routers_content = _routers_content.replace("$MultiBlocProviders$", _list_controller_register)
            with open(_routers_file, "w") as arquivo:
                arquivo.write(_routers_content)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsWebRouterInjectRootRouteBuilder: {error}"
            )
            return
