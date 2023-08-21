from pathlib import Path

from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class CustomDIOBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._target_file = Path(f"{self.command.flutter_dir}/lib/core/dio/custom_dio.dart")
        self._snippet_file = Path(f"{self.command.snippet_dir}/custom_dio.txt")

    def build(self):
        try:
            if Utils.check_file_is_locked(str(self._target_file)):
                return
            _content = self._parser_content()
            with open(self._target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_message(f"Erro ao executar o build de CustomDIOBuilder: {e}")
            return

    def _parser_content(self):
        return ParserContent(
            ["$project$"], [self.command.flutter_project], Utils.get_snippet(str(self._snippet_file))
        ).replace()
