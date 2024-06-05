import os
from pathlib import Path

from core.management.commands.constants.flutter import (
    DJANGO_TYPES,
    DJANGO_USER_FIELDS,
    FLUTTER_TYPES,
)
from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class ModelsBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self._path_flutter = self.app.path_flutter
        self._app_name = self.app.app_name
        self._model_name = self.app.model_name
        self._app_name_lower = self.app.app_name_lower
        self._model_name_lower = self.app.model_name_lower
        self._content_atributes = ""
        self._content_string_return = ""
        self._content_from_json = ""
        self._content_to_map = ""
        self._content_constructor = ""
        self._ignored_fields = ["enabled", "deleted", "createdOn", "updatedOn"]
        self._model_path_file = Path(
            f"{self._path_flutter}/lib/apps/{self._app_name_lower}/{self._model_name_lower}/model.dart"
        )
        self._snippet_model = Utils.get_snippet(
            str(Path(f"{self.snippet_dir}/model.txt"))
        )
        self._snippet_model = Utils.get_snippet(
            str(Path(f"{self.snippet_dir}/model.txt"))
        )

    def build(self):
        try:
            if Utils.check_file_is_locked(str(self._model_path_file)):
                Utils.show_error(f"File is locked: {self._model_path_file}")
                return
            for field in iter(self.app.model._meta.fields):
                _, _, _name = str(field).split(".")
                _name_dart = convert_to_camel_case(_name)

                if _name_dart in [f"id{self._model_name_lower}", "id"]:
                    continue

                _field_type = (
                    str(str(type(field)).split(".")[-1:])
                    .replace('["', "")
                    .replace("'>\"]", "")
                )

                _atribute = FLUTTER_TYPES[DJANGO_TYPES.index(_field_type)]

                if _name_dart not in ["enabled", "deleted", "createdOn", "updatedOn"]:
                    self._content_atributes += f"{_atribute} {_name_dart};\n  "

                if _name_dart not in DJANGO_USER_FIELDS:
                    self._content_string_return += (
                        f"{_name_dart.upper()}: ${_name_dart}\\n"
                    )

                if _name_dart not in self._ignored_fields:
                    default_value = None

                    if str(_atribute) == "int":
                        default_value = 0

                    if str(_atribute) == "double":
                        default_value = 0.0

                    if str(_atribute) == "bool":
                        default_value = "true"

                    if str(_atribute) == "String":
                        default_value = "''"

                    if str(_atribute) == "DateTime?":
                        self._content_constructor += f"DateTime? {_name_dart},"

                    if default_value is not None:
                        self._content_constructor += (
                            f"this.{_name_dart} = {default_value},\n"
                        )

                    if str(_atribute) == "DateTime?":
                        self._content_from_json += f"{_name_dart}: map.containsKey('{_name}')? Util.convertDate(map['{_name}']): null, \n"

                    elif str(_atribute) == "double":
                        self._content_from_json += (
                            f"{_name_dart}: map['{_name}'] ?? 0.0,\n{' ' * 8}"
                        )

                    elif str(_atribute) == "bool":
                        self._content_from_json += (
                            f"{_name_dart}: map['{_name}'] ?? false,\n{' ' * 8}"
                        )

                    else:
                        self._content_from_json += (
                            f"{_name_dart}: map['{_name}'] ?? '',\n{' ' * 8}"
                        )

                if _field_type in {"DateTimeField", "DateField", "TimeField"}:
                    return_types = {
                        "DateTimeField": "dt",
                        "DateField": "d",
                        "TimeField": "t",
                    }
                    self._content_to_map += f"'{_name}': Util.stringDateTimeSplit"
                    self._content_to_map += f"""({_name_dart}, returnType: '{return_types[_field_type]}'),\n{" " * 8}"""
                    continue

                self._content_to_map += f"'{_name}': {_name_dart},\n{' ' * 8}"

            if not Utils.check_file(self._model_path_file):
                os.makedirs(self._model_path_file)

            _content = self._parser_content()
            with open(self._model_path_file, "w", encoding="utf-8") as model_file:
                model_file.write(_content)

        except Exception as error:
            Utils.show_error(f"Error building models: {error}")
            raise error

    def _parser_content(self):
        return ParserContent(
            [
                "$ModelClass$",
                "$AttributeClass$",
                "$StringReturn$",
                "$Model$",
                "$ParserfromMap$",
                "$ParserToMap$",
                "$project$",
                "$ConstructorModelClass$",
            ],
            [
                self._model_name,
                self._content_atributes,
                self._content_string_return,
                self._model_name_lower,
                self._content_from_json,
                self._content_to_map,
                self.command.flutter_project,
                self._content_constructor,
            ],
            self._snippet_model,
        ).replace()
