from pathlib import Path

from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class AddPackagesWebBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._command_dir = Path(f"{self.command.path_command}/snippets/flutter_web_project/")
        self._snippet_dir = self.command.snippet_dir
        self._flutter_dir = self.command.flutter_dir
        self._project = self.command.project
        self._yaml_file_snippet = Path(f"{self._snippet_dir}/yaml.txt")

        self._yaml_file_target = Path(f"{self._flutter_dir}/pubspec.yaml")

    def build(self):
        """
        build _summary_
        """
        try:
            _snippet_content = Utils.get_snippet(str(self._yaml_file_snippet))
            with open(self._yaml_file_target, "w", encoding="utf-8") as _file:
                _content = ParserContent(
                    ["$AppPackage$", "$AppDescription$"],
                    [
                        self._project.lower(),
                        f"Projeto Flutter Web do sistema Django {self._project}",
                    ],
                    _snippet_content,
                ).replace()
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar o build de AddPackagesWebBuilder: {error}")
            return
