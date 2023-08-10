import os
from pathlib import Path

from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class DataServiceLayerBuild:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/cubit/")
        self._path_flutter = self.app.path_flutter
        self._app_name = self.app.app_name
        self._app_name_lower = self.app.app_name_lower
        self._model_name_lower = self.app.model_name_lower
        self._interface_path_file = Path(
            "{}/lib/apps/{}/{}/interface.dart".format(
                self._path_flutter,
                self._app_name_lower,
                self._model_name_lower,
            )
        )
        self._service_path_file = Path(
            "{}/lib/apps/{}/{}/service.dart".format(
                self._path_flutter,
                self._app_name_lower,
                self._model_name_lower,
            )
        )
        self._local_data_path_file = Path(
            "{}/lib/apps/{}/{}/data.dart".format(
                self._path_flutter,
                self._app_name_lower,
                self._model_name_lower,
            )
        )

    def build(self):
        self._parser_interface()
        self._parser_service()
        self._parser_local_data()

    def _parser_content(self, path_snippet, service=False):
        return ParserContent(
            ["$ModelClass$", "$App$", "$Model$", "$ModelClassCamelCase$", "$project$",],
            [
                self.app.model_name,
                self._app_name_lower,
                self._model_name_lower,
                convert_to_camel_case(self._app_name if service else self.app.model_name),
                self.command.flutter_project,
            ],
            path_snippet,
        ).replace()

    def _parser_interface(self):
        try:
            if Utils.check_file_is_locked(self._interface_path_file):
                Utils.show_message(f"File is locked: {self._interface_path_file}", title=True, border_color="red")
                return
            content = self._parser_content(Utils.get_snippet(str(Path(f"{self.snippet_dir}/interface.txt"))))
            with open(self._interface_path_file, "w", encoding="utf-8") as service_file:
                service_file.write(content)
            Utils.show_message(f"Builb interface to model: {self._app_name}")
        except Exception as error:
            raise error

    def _parser_service(self):
        try:
            if Utils.check_file_is_locked(self._service_path_file):
                Utils.show_message(f"File is locked: {self._service_path_file}", title=True, border_color="red")
                return
            content = self._parser_content(Utils.get_snippet(str(Path(f"{self.snippet_dir}/service.txt"))))
            with open(self._service_path_file, "w", encoding="utf-8") as service_file:
                service_file.write(content)
            Utils.show_message(f"Builb service to model: {self._app_name}")
        except Exception as error:
            raise error

    def _parser_local_data(self):
        try:
            if Utils.check_file_is_locked(self._local_data_path_file):
                Utils.show_message(f"File is locked: {self._local_data_path_file}", title=True, border_color="red")
                return
            content = self._parser_content(Utils.get_snippet(str(Path(f"{self.snippet_dir}/data.txt"))))
            with open(self._local_data_path_file, "w", encoding="utf-8") as service_file:
                service_file.write(content)
            Utils.show_message(f"Builb local data to model: {self._app_name}")
        except Exception as error:
            raise error
