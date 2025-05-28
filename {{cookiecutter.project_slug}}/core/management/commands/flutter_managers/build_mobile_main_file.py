from pathlib import Path

from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class MainFileMobileBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self.flutter_dir = self.command.flutter_dir
        self.project = self.command.project
        self.flutter_snippet = Path(f"{self.command.path_command}/snippets/flutter_mobile_project/")
        self._main_snippet = Path(f"{self.flutter_snippet}/main.dart")

        self._main_target = Path(f"{self.flutter_dir}/lib/main.dart")

    def build(self):
        """def para iniciar o processo de build"""
        try:
            _snippet_content = Utils.get_snippet(str(self._main_snippet))
            with open(self._main_target, "w", encoding="utf-8") as _file:
                _content = ParserContent(
                    ["$AppPackage$", "$AppDescription$"],
                    [
                        self.project.lower(),
                        f"Projeto Flutter Mobile do sistema Django {self.project}",
                    ],
                    _snippet_content,
                ).replace()
                _file.write(_content)

        except Exception as error:
            Utils.show_error(f"Erro ao executar build do main file: {error}")
