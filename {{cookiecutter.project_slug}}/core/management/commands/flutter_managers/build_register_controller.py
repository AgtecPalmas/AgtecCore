from base.settings import FLUTTER_APPS
from core.management.commands.utils import Utils


class RegisterProviderControllerBuilder:
    def __init__(self, command) -> tuple:
        self.command = command
        self._snippet_dir = self.command.snippet_dir
        self._flutter_dir = self.command.flutter_dir
        self._content = None
        self._imports = ""
        self._registers = ""

    def build(self) -> tuple:
        from core.management.commands.flutter import AppModel

        try:
            for _app in FLUTTER_APPS:
                _current_app = AppModel(self.command.flutter_project, _app)
                _app_name = _current_app.app_name
                _app_name_lower = _app_name.lower()
                for _model in _current_app.models:
                    _model_name_lower = _model[1].lower()
                    self._imports += f"import 'apps/{_app_name_lower}/{_model_name_lower}/controller.dart';\n"
                    self._registers += f"BlocProvider<{_model[1]}Controller>(create: (_) => {_model[1]}Controller(),),\n"
            self._imports += "import 'apps/auth/cubit.dart';\n"
            self._registers += (
                "BlocProvider<SettingsCubit>(create: (_) => SettingsCubit(),),\n"
            )
            self._registers += "BlocProvider<AuthCubit>(create: (_) => AuthCubit(),),\n"
            return self._imports, self._registers
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de RegisterControllerBuilder: {error}"
            )
            return None, None
