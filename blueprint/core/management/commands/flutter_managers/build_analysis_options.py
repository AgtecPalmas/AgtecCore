from pathlib import Path

from core.management.commands.utils import Utils


class AnalisysOptionsBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = self.command.snippet_dir
        self._flutter_dir = self.command.flutter_dir
        self._yaml_file_snippet = Path(f"{self._snippet_dir}/analysis_options.yaml")

        self._yaml_file_target = Path(f"{self._flutter_dir}/analysis_options.yaml")

    def build(self):
        """
        build _summary_
        """
        try:
            _snippet_content = Utils.get_snippet(str(self._yaml_file_snippet))
            with open(self._yaml_file_target, "w", encoding="utf-8") as _file:
                _file.write(_snippet_content)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AnalisysOptionsBuilder: {error}"
            )
            return
