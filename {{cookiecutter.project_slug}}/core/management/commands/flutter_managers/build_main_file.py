from pathlib import Path

from core.management.commands.flutter_managers.build_register_controller import RegisterProviderControllerBuilder
from core.management.commands.utils import Utils


class MainFileBuilder:
    def __init__(self, command, flutter_apps) -> None:
        self._command = command
        self._flutter_apps = flutter_apps
        self._snippet_dir = Path(f"{self._command.path_command}/snippets/flutter/cubit")
        self._target_file = Path(f"{self._command.flutter_dir}/lib/main.dart")
        self._snippet_file = Path(f"{self._snippet_dir}/main.txt")
        self._import_controllers = ""
        self._import_views = ""
        self._register_controller = ""

    def _mapping_all_application(self):
        from core.management.commands.flutter import AppModel

        try:
            _imports_views = ""
            _imports_controllers = ""
            _controllers_models = ""
            _list_views = ""
            _current_app = None

            for app in self._flutter_apps:
                _current_app = AppModel(self._command.flutter_project, app)
                _app = _current_app.app_name
                for model in _current_app.models:
                    _model = model[1]
                    _app_model = f"{_app.title()}{_model}"
                    _imports_views += f"import 'apps/{_app}/{_model.lower()}/pages/list.dart' as {_app_model}Views;\n"
                    _list_views += f"Itens(title: '{model[0]._meta.verbose_name}', "
                    _list_views += f"icon: FontAwesomeIcons.folderOpen, uri: {_app.title()}{_model}."
                    _list_views += f"{_model}ListPage()),\n"
                    _imports_controllers += f"import 'apps/{_app.lower()}/{_model.lower()}/controller.dart' "
                    _imports_controllers += f"as {_app.title()}{_model.title()}Controller;\n"
                    __controller_model = f"{_app.title()}{_model.title()}Controller.{_model}"
                    _controllers_models += f"getIt.registerSingleton<{__controller_model}Controller>"
                    _controllers_models += f"({__controller_model}Controller(), instanceName: "
                    _controllers_models += f"'{_app.title()}{_model.title()}Controller');\n    "

            return _imports_views, _imports_controllers, _controllers_models, _list_views

        except Exception as error:
            Utils.show_error(f"Error: {error}")

    def _build_menu_home_page_items(self):
        from core.management.commands.flutter import AppModel

        try:
            _items_menu = ""
            for app in self._flutter_apps:
                _current_app = AppModel(self._command.flutter_project, app)
                _app = _current_app.app_name
                for model in _current_app.models:
                    _model = model[1]
                    _items_menu += f"list.add(Itens(title: '{_model.title()}'"
                    _items_menu += f",icon: FontAwesomeIcons.folderOpen,uri: {_app.title()}{_model}"
                    _items_menu += f"Views.{_model}ListPage(),),);"
            return _items_menu
        except Exception as error:
            Utils.show_error(f"Error in _build_menu_home_page_itens: {error}")

    def _build_main_file(self):
        try:
            self._import_controllers += "import 'apps/configuracao/model.dart';"
            self._import_views += "import 'apps/configuracao/index.page.dart';\n"
            self._register_controller += "getIt.registerSingleton<SettingsController>(SettingsController());"
            if Utils.check_file_is_locked(self._target_file):
                return

            _imports, _controllers, _registers, _views = self._mapping_all_application()

            _controllers += "import 'apps/configuracao/model.dart';"
            _imports += "import 'apps/configuracao/index.page.dart';\n"
            _registers += "getIt.registerSingleton<SettingsController>(SettingsController());"

            if _imports is None or _controllers is None:
                return

            _snippet = Utils.get_snippet(self._snippet_file)
            _snippet_content = _snippet.replace("$project$", self._command.flutter_project)

            _controllers += "import 'apps/configuracao/cubit.dart"

            _import, _register = RegisterProviderControllerBuilder(command=self._command).build()

            _snippet_content = _snippet_content.replace("$ImportController$", _controllers)
            _snippet_content = _snippet_content.replace("$ImportCubit$", _import)
            _snippet_content = _snippet_content.replace("$RegisterProviders$", _register)

            _snippet_content = _snippet_content.replace("$Listviews$", _views)
            with open(self._target_file, "w", encoding="utf-8") as _file:
                _file.write(_snippet_content)

            self._build_home_page(_imports)

        except Exception as error:
            Utils.show_error(f"Erro ao executar build do main file: {error}")

    def _build_home_page(self, imports):
        try:
            if imports is None:
                Utils.show_error("Erro ao executar o _build_home_page, imports vazio")
                return

            _target_page_file = Path(f"{self._command.flutter_dir}/lib/home.page.dart")
            _snippet_page_file = Path(f"{self._snippet_dir}/home.page.txt")
            _content = ""

            if Utils.check_file_is_locked(_target_page_file):
                return

            _menu_itens = self._build_menu_home_page_items()

            _content = Utils.get_snippet(_snippet_page_file)
            _content = _content.replace("$ImportViews$", imports)
            _content = _content.replace("$ItenMenu$", _menu_itens)

            with open(_target_page_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build home page file: {error}")

    def build(self):
        """Método para iniciar o processo de build"""
        try:
            self._build_main_file()
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do main file: {error}")
