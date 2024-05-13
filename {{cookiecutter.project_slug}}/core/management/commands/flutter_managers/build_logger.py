from pathlib import Path

from core.management.commands.utils import Utils


class LoggerBuilder:
    def __init__(self, command) -> None:
        self.command = command
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._log_path_file = Path(f"{self.command.core_dir}/agtec.logger.dart")

    def build(self):
        """
        build _summary_
        """
        try:
            _content = Utils.get_snippet(
                str(Path(f"{self._snippet_dir}/agtec.logger.txt"))
            )
            with open(self._log_path_file, "w", encoding="utf-8") as logger_file:
                logger_file.write(_content)
        except Exception as error:
            Utils.show_message(f"Erro ao executar o build de LoggerBuilder: {error}")
            return
