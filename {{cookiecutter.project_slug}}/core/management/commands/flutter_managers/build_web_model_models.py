"""
Build para gerenciar a criação dos arquivos da camanda de models
de cada model da App, que serão criados dentro do diretório
models

"""
from pathlib import Path

from core.management.commands.constants.flutter import (
    DJANGO_TYPES,
    DJANGO_USER_FIELDS,
    FLUTTER_TYPES,
)
from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class AppsWebModelBuilder:
    def __init__(self, command, app, model=None) -> None:
        self.command = command
        self.app = app
        self.model = model
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/")
        self.flutter_web_dir = self.command.flutter_dir
        self._path_flutter = self.command.flutter_dir
        self._app_name = self.app.name
        self._content_atributes = ""
        self._content_string_return = ""
        self._content_from_json = ""
        self._content_to_map = ""
        self._attributes_constructor_copy_with = ""
        self._attributes_copy_with = ""
        self._content_constructor = ""
        self._ignored_fields = ["enabled", "deleted", "createdOn", "updatedOn"]
        self.flutter_model_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_web_project/layers/model.txt"
        )

    def build(self):
        try:
            # Pegando os models da app
            _models_app = self.app.get_models()
            for model in _models_app:
                _model_app = self.app.name
                _model_app_lower = _model_app.lower()
                _model_name = model.__name__
                _model_name_lower = _model_name.lower()
                _app_file = Path(
                    f"{self.flutter_web_dir}/lib/apps/{_model_app_lower}/models/{_model_name_lower}.dart"
                )
                _list_fields_parser = []

                if self.model is not None and _model_name_lower != self.model.lower():
                    continue 

                # Verificando se o arquivo já existe e está bloqueado
                if Utils.check_file_is_locked(str(_app_file)):
                    return

                for field in iter(model._meta.fields):
                    _, _, _name = str(field).split(".")
                    _name_dart = convert_to_camel_case(_name)

                    if _name_dart in [f"id{_model_app_lower}", "id"]:
                        continue
                    
                    # Verificando se o campo já foi parseado
                    if _name_dart in _list_fields_parser:
                        continue

                    _field_type = (
                        str(str(type(field)).split(".")[-1:])
                        .replace('["', "")
                        .replace("'>\"]", "")
                    )

                    _atribute = FLUTTER_TYPES[DJANGO_TYPES.index(_field_type)]

                    if _name_dart not in [
                        "enabled",
                        "deleted",
                        "createdOn",
                        "updatedOn",
                    ]:
                        
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

                        # Criando os atributos do construtor do método copyWith
                        if '?' in str(_atribute):
                            self._attributes_constructor_copy_with += f"{_atribute} {_name_dart},\n{' ' * 8}"
                        else:
                            self._attributes_constructor_copy_with += f"{_atribute}? {_name_dart},\n{' ' * 8}"
                        self._attributes_copy_with += f"{_name_dart}: {_name_dart} ?? this.{_name_dart},\n{' ' * 8}"

                        if str(_atribute) == "DateTime?":
                            self._content_constructor += f"DateTime? {_name_dart},"

                        if default_value is not None:
                            self._content_constructor += (
                                f"this.{_name_dart} = {default_value},\n"
                            )

                        if str(_atribute) == "DateTime?":
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? DateFormat('yyyy-MM-dd').parse(map['{_name}']): null; \n"

                        elif _name_dart == "djangoUser":
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? map['{_name}'] ?? 0: 0;\n{' ' * 8}"

                        elif (
                            str(_atribute) == "DateField?"
                            or str(_atribute) == "DateField"
                        ):
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? DateFormat('yyyy-MM-dd').parse(map['{_name}']): null; \n"

                        elif str(_atribute) == "double":
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? map['{_name}'] ?? 0.0: 0.0;\n{' ' * 8}"

                        elif str(_atribute) == "bool":
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? map['{_name}'] ?? false: false;\n{' ' * 8}"

                        else:
                            self._content_from_json += f"model.{_name_dart} = map.containsKey('{_name}')? map['{_name}'] ?? '': '';\n{' ' * 8}"

                    if _field_type in {"DateTimeField", "DateField", "TimeField"}:
                        self._content_to_map += f"'{_name}': {_name_dart} != null ? DateFormat('dd/MM/yyyy HH:mm:ss').format({_name_dart}!) : null,\n{' ' * 8}"
                        continue

                    self._content_to_map += f"'{_name}': {_name_dart},\n{' ' * 8}"

                self._model_name = _model_name.title()
                self._model_name_lower = _model_name_lower.lower()
                _content = self._parser_content(model)
                with open(_app_file, "w", encoding="utf-8") as model_file:
                    model_file.write(_content)

                # Limpando os atributos para o próximo model
                self._content_atributes = ""
                self._content_string_return = ""
                self._content_from_json = ""
                self._content_to_map = ""
                self._attributes_constructor_copy_with = ""
                self._attributes_copy_with = ""
                self._content_constructor = ""

        except Exception as error:
            Utils.show_error(f"Error building models: {error}")
            raise error

    def _parser_content(self, model):
        _snippet_content = Utils.get_snippet(str(self.flutter_model_snippet))
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
                "$AttributeClassConstructor$",
                "$AttributesClassCopyWith$",
            ],
            [
                model.__name__,
                self._content_atributes,
                self._content_string_return,
                self._model_name_lower,
                self._content_from_json,
                self._content_to_map,
                self.command.flutter_project,
                self._content_constructor,
                self._attributes_constructor_copy_with,
                self._attributes_copy_with,
            ],
            _snippet_content,
        ).replace()
