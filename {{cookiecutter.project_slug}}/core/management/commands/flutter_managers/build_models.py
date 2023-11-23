import os
from pathlib import Path

from core.management.commands.constants.flutter import DJANGO_TYPES, DJANGO_USER_FIELDS, FLUTTER_TYPES
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
        self._ignored_fields = ["enabled", "deleted", "deletedOn", "createdOn", "updatedOn"]
        self._model_path_file = Path(
            "{}/lib/apps/{}/{}/model.dart".format(
                self._path_flutter,
                self._app_name_lower,
                self._model_name_lower,
            )
        )
        self._snippet_model = Utils.get_snippet(str(Path(f"{self.snippet_dir}/model.txt")))

    def build(self):
        try:
            if Utils.check_file_is_locked(str(self._model_path_file)):
                Utils.show_error(f"File is locked: {self._model_path_file}")
                return
            for field in iter(self.app.model._meta.fields):
                _app, _model, _name = str(field).split(".")
                _name_dart = convert_to_camel_case(_name)
                if _name_dart in [f"id{self._model_name_lower}", "id"]:
                    continue
                _field_type = str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")
                _atribute = FLUTTER_TYPES[DJANGO_TYPES.index(_field_type)]
                if _name_dart not in ["enabled", "deleted", "deletedOn", "createdOn", "updatedOn"]:
                    self._content_atributes += f"{_atribute} {_name_dart};\n  "
                if _name_dart not in DJANGO_USER_FIELDS:
                    self._content_string_return += f"{_name_dart.upper()}: ${_name_dart}\\n"
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
                        self._content_constructor += "this.{} = {},\n".format(_name_dart, default_value)

                if _name_dart not in self._ignored_fields:
                    if str(_atribute) == "DateTime?":
                        self._content_from_json += (
                            "{}: map.containsKey('{}')? Util.convertDate(map['{}']): null, \n".format(
                                _name_dart, _name, _name
                            )
                        )
                        # self._content_from_json += "? null:  Util.convertDate(map['{}']),\n".format(_name, " " * 8)
                    elif str(_atribute) == "double":
                        self._content_from_json += "{1}: map['{2}'] ?? 0.0,\n{0}".format(" " * 8, _name_dart, _name)
                    elif str(_atribute) == "bool":
                        self._content_from_json += "{1}: map['{2}'] ?? false,\n{0}".format(" " * 8, _name_dart, _name)
                    else:
                        if _name_dart.startswith("fk"):
                            self._content_from_json += "{1}: map['{2}'] ?? '',\n{0}".format(" " * 8, _name_dart, _name)
                        else:
                            self._content_from_json += "{1}: map['{2}'] ?? '',\n{0}".format(" " * 8, _name_dart, _name)

                if str(_field_type) == "DateTimeField":
                    self._content_to_map += "'{}': Util.stringDateTimeSplit".format(_name)
                    self._content_to_map += "({}, returnType: 'dt'),\n{}".format(_name_dart, " " * 8)
                    continue
                if str(_field_type) == "DateField":
                    self._content_to_map += "'{}': Util.stringDateTimeSplit".format(_name)
                    self._content_to_map += "({}, returnType: 'd'),\n{}".format(_name_dart, " " * 8)
                    continue
                if str(_field_type) == "TimeField":
                    self._content_to_map += "'{}': Util.stringDateTimeSplit".format(_name)
                    self._content_to_map += "({}, returnType: 't'),\n{}".format(_name_dart, " " * 8)
                    continue
                if str(_field_type) in ["FloatField", "DecimalField"]:
                    self._content_to_map += "'{0}': {1},\n{2}".format(_name, _name_dart, " " * 8)
                    continue
                if str(_atribute) == "bool":
                    self._content_to_map += "'{0}': {1},\n{2}".format(_name, _name_dart, " " * 8)
                    continue
                self._content_to_map += "'{0}': {1},\n{2}".format(_name, _name_dart, " " * 8)

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
