import os
from pathlib import Path

from core.management.commands.utils import Utils


class TranslateStringBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._lang_dir = Path(f"{self.command.flutter_dir}/lang")
        self._pt_br_file = Path(f"{self.command.flutter_dir}/lang/pt.json")  # OK
        self._en_us_file = Path(f"{self.command.flutter_dir}/lang/en.json")  # OK
        self._path_localization_file = os.path.join(self.command.core_dir, "localization.dart")
        self._snippet_file = Utils.get_snippet(str(Path(f"{self.snippet_dir}/localization.txt")))

    def build(self):
        try:
            if Utils.check_file_is_locked(str(self._path_localization_file)):
                return

            with open(self._path_localization_file, "w", encoding="utf-8") as localizations:
                localizations.write(self._snippet_file)

            if not Utils.check_dir(self._lang_dir):
                os.makedirs(self._lang_dir)

            if not Utils.check_file(self._pt_br_file):
                _snippet = Utils.get_snippet(str(Path(f"{self.snippet_dir}/pt_language.txt")))
                with open(self._pt_br_file, "w", encoding="utf-8") as pt_file:
                    pt_file.write(_snippet)

            if not Utils.check_file(self._en_us_file):
                _snippet = Utils.get_snippet(str(Path(f"{self.snippet_dir}/en_language.txt")))
                with open(self._en_us_file, "w", encoding="utf-8") as en_file:
                    en_file.write(_snippet)
        except Exception as e:
            Utils.show_message(f"Erro ao executar o build de TranslateStringBuilder: {e}")
            return
