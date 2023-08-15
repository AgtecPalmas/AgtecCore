from pathlib import Path

from core.management.commands.utils import Utils


class SettingsControllerBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._command_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._snippet_dir = self.command.snippet_dir
        self._settings_page_snippet = Path(f"{self._snippet_dir}/cubit/settings_page.txt")
        self._settings_page_target = self.command.app_configuration_page_file
        
        self._settings_controller_snippet = Path(f"{self._snippet_dir}/cubit/settings.txt")
        self._settings_controller_target = self.command.app_configuration_cubit_file

        self._settings_state_snippet = Path(f"{self._snippet_dir}/cubit/settings_state.txt")
        self._settings_state_target = self.command.app_configuration_cubit_state_file

    def build(self):
        """
        build _summary_
        """
        try:
            self._parser_page()
            self._parser_settings_controller()
            self._parser_settings_state()
        except Exception as error:
            Utils.show_error(f"Erro ao executar o build de SettingsControllerBuilder: {error}")
            return

    def _parser_page(self):
        try:
            if Utils.check_file_is_locked(self._settings_page_target):
                return
            _content = Utils.get_snippet(str(self._settings_page_snippet))
            with open(self._settings_page_target, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar o _parser_config_file do SettingsControllerBuilder: {error}")
            return

    def _parser_settings_controller(self):
        try:
            if Utils.check_file_is_locked(self._settings_controller_target):
                return
            _content = Utils.get_snippet(str(self._settings_controller_snippet))
            with open(self._settings_controller_target, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as erro:
            Utils.show_error(f"Erro ao executar o _parser_settings do SettingsControllerBuilder: {erro}")
            return

    def _parser_settings_state(self):
        try:
            if Utils.check_file_is_locked(self._settings_state_target):
                return
            _content = Utils.get_snippet(str(self._settings_state_snippet))
            with open(self._settings_state_target, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar o _parser_settings do SettingsControllerBuilder: {error}")
            return
