from pathlib import Path

from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class ControllerBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/cubit/")
        self._path_flutter = self.app.path_flutter
        self._app_name = self.app.app_name
        self._app_name_lower = self.app.app_name_lower
        self._model_name_lower = self.app.model_name_lower
        self._controller_path_file = Path(
            f"{self._path_flutter}/lib/apps/{self._app_name_lower}/{self._model_name_lower}/controller.dart"
        )
        self._controller_state_path_file = Path(
            f"{self._path_flutter}/lib/apps/{self._app_name_lower}/{self._model_name_lower}/state.dart"
        )

    def build(self):
        """
        build _summary_

        Raises
        ------
        error
            _description_
        """
        Utils.show_message(
            f"Building controller layer from: {self._app_name} | {self._model_name_lower}",
        )
        try:
            self._parser_controller()
            self._parser_controller_state()
        except Exception as error:
            raise error

    def _parser_content(self, path_snippet):
        return ParserContent(
            ["$ModelClass$", "$ModelClassCamelCase$"],
            [self.app.model_name, convert_to_camel_case(self.app.model_name)],
            path_snippet,
        ).replace()

    def _parser_controller(self):
        try:
            if Utils.check_file_is_locked(str(self._controller_path_file)):
                Utils.show_error(f"File is locked: {self._controller_path_file}")
                return
            _snippet = Utils.get_snippet(str(Path(f"{self.snippet_dir}/controller.txt")))
            _content = self._parser_content(_snippet)
            with open(self._controller_path_file, "w", encoding="utf-8") as file:
                file.write(_content)
        except Exception as error:
            raise error

    def _parser_controller_state(self):
        try:
            if Utils.check_file_is_locked(str(self._controller_state_path_file)):
                Utils.show_error(f"File is locked: {self._controller_state_path_file}")
                return
            _snippet = Utils.get_snippet(str(Path(f"{self.snippet_dir}/state.txt")))
            _content = self._parser_content(_snippet)
            with open(self._controller_state_path_file, "w", encoding="utf-8") as file:
                file.write(_content)
        except Exception as error:
            raise error
