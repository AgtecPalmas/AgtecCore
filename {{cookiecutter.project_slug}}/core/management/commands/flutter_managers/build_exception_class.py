from pathlib import Path

from core.management.commands.utils import Utils


class ExceptionClassBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._target_file = Path(f"{self.command.flutter_dir}/lib/core/exceptions/exception.dart")
        self._snippet_file = Path(f"{self.command.snippet_dir}/exception.txt")

    def build(self):
        try:
            if Utils.check_file_is_locked(self._target_file):
                return
            _content = Utils.get_snippet(str(self._snippet_file))
            with open(self._target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de ExceptionClassBuilder: {e}")
            return
