from pathlib import Path

from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class WidgetBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._path_flutter = self.app.path_flutter
        self._app_name_lower = self.app.app_name_lower
        self._model_name = self.app.model_name
        self._model_name_lower = self.app.model_name_lower
        self._snippet_file = Path(f"{self.command.snippet_dir}/widget.txt")
        self._target_file = Path(
            "{}/lib/apps/{}/{}/pages/widget.dart".format(
                self._path_flutter, self._app_name_lower, self._model_name_lower
            )
        )

    def build(self):
        try:
            if Utils.check_file_is_locked(str(self._target_file)):
                return
            _content = self._parser_content()
            with open(self._target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de WidgetBuilder: {e}")
            return

    def _parser_content(self):
        return ParserContent(
            ["$ModelClass$"],
            [self._model_name],
            Utils.get_snippet(str(self._snippet_file)),
        ).replace()
