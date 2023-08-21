from pathlib import Path

from core.management.commands.utils import Utils


class CustomDIOInterceptorsBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._target_dir = Path(f"{self.command.flutter_dir}/lib/core/dio/interceptors/")
        self._header_token_interceptor = Path(f"{self._target_dir}/header_token_interceptor.dart")
        self._header_token_snippet = Path(f"{self._snippet_dir}/dio_interceptor_header.txt")

        self._refresh_token_interceptor = Path(f"{self._target_dir}/refresh_token_interceptor.dart")
        self._refresh_token_snippet = Path(f"{self._snippet_dir}/dio_interceptor_token.txt")

    def build(self):
        try:
            self._build_header_interceptor()
            self._build_refresh_token_interceptor()
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de CustomDIOInterceptorsBuilder: {e}")
            return

    def _build_header_interceptor(self):
        try:
            if Utils.check_file_is_locked(str(self._header_token_interceptor)):
                return
            _content = Utils.get_snippet(str(self._header_token_snippet))
            with open(self._header_token_interceptor, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de _build_header_interceptor: {e}")
            return

    def _build_refresh_token_interceptor(self):
        try:
            if Utils.check_file_is_locked(str(self._refresh_token_interceptor)):
                return
            _content = Utils.get_snippet(str(self._refresh_token_snippet))
            with open(self._refresh_token_interceptor, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de _build_refresh_token_interceptor: {e}")
            return
