from pathlib import Path

from core.management.commands.utils import Utils


class StringExtensionsBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._path_file = self.command.ui_string_extensions_file

    def build(self):
        try:
            _content = Utils.get_snippet(
                str(Path(f"{self._snippet_dir}/agtec.string_methods_extensions.txt"))
            )
            with open(self._path_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_message(f"Erro ao executar o build de LoggerBuilder: {e}")
            return
