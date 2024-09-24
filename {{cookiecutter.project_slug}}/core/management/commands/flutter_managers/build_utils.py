from pathlib import Path

from base.settings import (
    FLUTTER_API_PASSWORD_DEV,
    FLUTTER_API_PATH,
    FLUTTER_API_USER_DEV,
    SYSTEM_NAME,
)
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class UtilsBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._command_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._snippet_dir = self.command.snippet_dir
        self._config_snippet_file = Path(f"{self._snippet_dir}/config.txt")
        self._config_target_file = Path(f"{self.command.config_file}")
        self._either_snippet_file = Path(f"{self._snippet_dir}/either.txt")
        self._either_target_file = Path(f"{self.command.either_file}")
        self._application_config_snippet_file = Path(f"{self._snippet_dir}/application.config.txt")
        self._application_config_target_file = Path(f"{self.command.application_config_file}")
        self._util_snippet_file = Path(f"{self._snippet_dir}/util.txt")
        self._util_target_file = Path(f"{self.command.util_file}")

    def build(self):
        try:
            self._parser_config_file()
            self._parser_util_file()
            self._parser_either_file()
            self._parser_application_config_file()
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de UtilsBuilder: {e}")
            return
        
    def _get_real_ip_address(self):
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception as e:
            Utils.show_error(f"Erro ao executar o _get_real_ip_address do UtilsBuilder: {e}")
            return 

    def _parser_config_file(self):
        try:
            if Utils.check_file_is_locked(str(self._config_target_file)):
                return
            _current_ip = self._get_real_ip_address()
            if _current_ip is None:
                _current_ip = "0.0.0.0"
            _content = ParserContent(
                [
                    "$AppName$",
                    "$DjangoAPIPath$",
                    "$UriAPIDeveloper$",
                    "$FastAPIPasswordDevelopment$",
                    "$FastAPIUserDevelopment$",
                    "$IpAddress$",
                ],
                [
                    SYSTEM_NAME,
                    FLUTTER_API_PATH,
                    FLUTTER_API_PATH,
                    FLUTTER_API_PASSWORD_DEV,
                    FLUTTER_API_USER_DEV,
                    _current_ip,
                ],
                Utils.get_snippet(str(self._config_snippet_file)),
            ).replace()
            with open(self._config_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_config_file do UtilsBuilder: {e}"
            )
            return

    def _parser_either_file(self):
        try:
            if Utils.check_file_is_locked(str(self._either_target_file)):
                return

            _content = Utils.get_snippet(str(self._either_snippet_file))
            with open(self._either_target_file, "w", encoding="utf-8") as _either_file:
                _either_file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_either_file do UtilsBuilder: {e}"
            )
            return

    def _parser_application_config_file(self):
        try:
            if Utils.check_file_is_locked(str(self._application_config_target_file)):
                return

            _content = Utils.get_snippet(str(self._application_config_snippet_file))
            with open(self._application_config_target_file, "w", encoding="utf-8") as _either_file:
                _either_file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_either_file do UtilsBuilder: {e}"
            )
            return

    def _parser_util_file(self):
        try:
            if Utils.check_file_is_locked(str(self._util_target_file)):
                return
            _content = ParserContent(
                ["$AppName$", "$DjangoAPIPath$"],
                [SYSTEM_NAME, FLUTTER_API_PATH],
                Utils.get_snippet(str(self._util_snippet_file)),
            ).replace()
            with open(self._util_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(
                f"Erro ao executar o _parser_util_file do UtilsBuilder: {e}"
            )
            return
