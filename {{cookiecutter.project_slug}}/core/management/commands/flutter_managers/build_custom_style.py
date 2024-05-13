from pathlib import Path

from core.management.commands.utils import Utils


class CustomStyleBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._path_file = Path(f"{self.command.ui_dir}/custom.style.dart")

    def build(self):
        try:
            _content = Utils.get_snippet(
                str(Path(f"{self._snippet_dir}/custom.style.txt"))
            )
            with open(self._path_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_message(f"Erro ao executar o build de CustomStyleBuilder: {e}")
            return
