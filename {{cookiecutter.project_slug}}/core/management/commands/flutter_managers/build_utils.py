from pathlib import Path

from base.settings import API_PATH, SYSTEM_NAME
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class UtilsBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._command_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._snippet_dir = self.command.snippet_dir
        self._config_snippet_file = Path(f"{self._snippet_dir}/config.txt")
        self._config_target_file = Path(f"{self.command.config_file}")
        self._util_snippet_file = Path(f"{self._snippet_dir}/util.txt")
        self._util_target_file = Path(f"{self.command.util_file}")

    def build(self):
        try:
            self._parser_config_file()
            self._parser_util_file()
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de UtilsBuilder: {e}")
            return

    def _parser_config_file(self):
        try:
            if Utils.check_file_is_locked(str(self._config_target_file)):
                return
            _content = ParserContent(
                ["$AppName$", "$DjangoAPIPath$"],
                [SYSTEM_NAME, API_PATH],
                Utils.get_snippet(str(self._config_snippet_file)),
            ).replace()
            with open(self._config_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_config_file do UtilsBuilder: {e}"
            )
            return

    def _parser_util_file(self):
        try:
            if Utils.check_file_is_locked(str(self._util_target_file)):
                return
            _content = ParserContent(
                ["$AppName$", "$DjangoAPIPath$"],
                [SYSTEM_NAME, API_PATH],
                Utils.get_snippet(str(self._util_snippet_file)),
            ).replace()
            with open(self._util_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_util_file do UtilsBuilder: {e}"
            )
            return
