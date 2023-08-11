from pathlib import Path

from core.management.commands.constants.flutter import DJANGO_TYPES, FLUTTER_TYPES
from core.management.commands.flutter_managers.utils import convert_to_camel_case, ignore_base_fields
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class PagesBuilder:
    def __init__(self, command, source_app) -> None:
        self.command = command
        self._source_app = source_app
        self._model_name_lower = self._source_app.model_name_lower
        self._app_name_lower = self._source_app.app_name_lower
        self._snippet_dir = Path(f"{self.command.path_command}/snippets/flutter/cubit")
        self._pages_target_path = (
            f"{self._source_app.path_flutter}/lib/apps/{self._app_name_lower}/{self._model_name_lower}/pages/"
        )

    def build(self):
        """
        Método responsável por executar o build das pages
        """
        try:
            self._build_index_page()
            self._build_detail_page()
            self._build_list_page()
            self._build_create_or_update_page()
            self._build_create_or_update_page(update=True)
        except Exception as error:
            Utils.show_error(f"Ocorreu o erro: {error} ao executar o build do PagesBuilder")

    def _get_controllers_data(self, attribute, model_name, name, name_title) -> str:
        _controllers_data = ""
        _space = " " * 16
        _model_cc = convert_to_camel_case(model_name)
        _title = name_title
        try:
            if attribute == "int":
                if f"id{model_name.lower()}" == name.lower():
                    _controllers_data = (
                        f"{_space}_{_model_cc}Model.id = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
                    )
                else:
                    _controllers_data = (
                        f"{_space}_{_model_cc}Model.{name} = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
                    )
            elif attribute == "double":
                _controllers_data = (
                    f"{_space}_{_model_cc}Model.{name} = double.tryParse(_{_model_cc}Form{_title}.text) ?? 0.0;\n"
                )
            elif attribute == "bool":
                _field_is_empty = f"_{_model_cc}Form{_title}.text.isNotEmpty"
                _fields_contains_zero = f"_{_model_cc}Form{_title}.text.contains('0') ? true: false : false"
                _controllers_data = f"{_space}_{_model_cc}Model.{name} = {_field_is_empty} ? {_fields_contains_zero};\n"
            elif attribute == "DateTime?":
                _controllers_data = f'{_space}_{_model_cc}Model.{name} = _{_model_cc}Form{_title}.text != ""?'
                _controllers_data += f" Util.convertDate(_{_model_cc}Form{_title}.text) : null;\n"
            else:
                _controllers_data = f"{_space}_{_model_cc}Model.{name} = _{_model_cc}Form{_title}.text;\n"
            return _controllers_data
        except Exception as error:
            Utils.show_error(
                f"Error in __get_controllers_data: {error}",
            )
            return _controllers_data

    def _get_attributes_data(self, attribute, model_name, name, name_title) -> str:
        _attribute = ""
        _space = " " * 16
        _model_cc = convert_to_camel_case(model_name)
        _title = name_title
        try:
            if attribute == "int":
                if f"id{model_name.lower()}" == name.lower():
                    _attribute = f"{_space}_{_model_cc}Model.id = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
                else:
                    _attribute = (
                        f"{_space}_{_model_cc}Model.{name} = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
                    )

            elif attribute == "double":
                _attribute = (
                    f"{_space}_{_model_cc}Model.{name} = double.tryParse(_{_model_cc}Form{_title}.text) ?? 0.0;\n"
                )
            elif attribute == "bool":
                _check_field = f"_{_model_cc}Form{_title}.text.isNotEmpty"
                _i_contains = f"_{_model_cc}Form{_title}.text.contains('0') ? true: false : false"
                _attribute = f"{_space}_{_model_cc}Model.{name} = {_check_field} ? {_i_contains};\n"
            elif attribute == "DateTime?":
                _convert = f"?Util.convertDate(_{_model_cc}Form{name_title}.text): null"
                _attribute = f"{_space}_{_model_cc}Model.{name} = "
                _attribute += f'_{_model_cc}Form{name_title}.text != "" {_convert};\n'
            else:
                _attribute = f"{_space}_{_model_cc}Model.{name} = _{_model_cc}Form{name_title}.text;\n"
            return _attribute
        except Exception as error:
            Utils.show_error(f"Error in __get_attributes: {error}")
            return None

    def _to_camel_case(self, text, flutter=False):
        try:
            components = text.split("_")
            if flutter is True:
                if len(components) == 1:
                    _string = components[0]
                    return f"{_string[:1].lower()}{_string[1:]}"
                return components[0] + "".join(x.title() for x in components[1:])
            return components[0] + "".join(x.title() for x in components[1:])
        except Exception as error:
            Utils.show_message(f"Error in Camel Case: {error}")
            return None

    def _build_create_or_update_page(self, update=False):
        try:
            _target_file = Path(f"{self._pages_target_path}/create.dart")
            _snippet_file = Path(f"{self._snippet_dir}/create_page.txt")

            if update is True:
                _target_file = Path(f"{self._pages_target_path}/update.dart")
                _snippet_file = Path(f"{self._snippet_dir}/update_page.txt")

            _form_content_file = Path(f"{self._snippet_dir}/text_field.txt")
            if Utils.check_file_is_locked(_target_file):
                return
            _content_attributes = ""
            _text_fields = ""
            _attributes_data = ""
            _clear_data = ""
            _edited_attributes = ""
            _get_controllers_data = ""
            _snippet_content = Utils.get_snippet(_snippet_file)
            _content_form = Utils.get_snippet(_form_content_file)

            for field in iter(self._source_app.model._meta.fields):  # noqa W0212
                _, __, _name = str(field).split(".")
                _name_title = self._to_camel_case(_name.title())
                _name = self._to_camel_case(_name.lower())

                if ignore_base_fields(_name):
                    continue

                field_type = str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")

                attribute = FLUTTER_TYPES[DJANGO_TYPES.index(field_type)]
                _model_name_camel_case = convert_to_camel_case(self._source_app.model_name)
                _content_attributes += (
                    f"  final _{_model_name_camel_case}Form{_name_title} = TextEditingController();\n"
                )
                text_field = _content_form
                controller = f"_{_model_name_camel_case}Form{_name_title}"
                text_field = text_field.replace("$controller$", controller)
                text_field = text_field.replace("$Field$", str(field.verbose_name).replace("R$", r"R\$"))
                _text_fields += text_field
                _attributes_data += self._get_attributes_data(
                    attribute, self._source_app.model_name, _name, _name_title
                )
                _get_controllers_data += self._get_controllers_data(
                    attribute, self._source_app.model_name, _name, _name_title
                )
                _clear_data += f"    {controller}.clear();\n"

                if _name.startswith(f"id{self._source_app.model_name_lower}"):
                    _name = "id"

                _edited_attributes += f"      {controller}.text = _{_model_name_camel_case}Model.{_name}.toString();\n"

            content = ParserContent(
                [
                    "$app$",
                    "$App$",
                    "$Model$",
                    "$model$",
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                    "$project$",
                    "$Attributes$",
                    "$Form$",
                    "$AttributesData$",
                    "$ClearData$",
                    "$EditedAttributes$",
                    "$GetValuesControllers$",
                ],
                [
                    self._source_app.app_name_lower,
                    self._source_app.app_name_lower,
                    convert_to_camel_case(self._source_app.model_name),
                    self._source_app.model_name_lower,
                    self._source_app.model_name,
                    convert_to_camel_case(self._source_app.model_name),
                    self.command.flutter_project,
                    _content_attributes,
                    _text_fields,
                    _attributes_data,
                    _clear_data,
                    _edited_attributes,
                    _get_controllers_data,
                ],
                _snippet_content,
            ).replace()

            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(content)
        except Exception as error:
            Utils.show_error(f"Ocorreu o erro: {error} ao executar o _build_create_update_page do PagesBuilder")

    def _build_detail_page(self):
        try:
            _target_file = Path(f"{self._pages_target_path}/detail.dart")
            _snippet_file = Path(f"{self._snippet_dir}/detail_page.txt")
            if Utils.check_file_is_locked(_target_file):
                return
            _snippet_content = Utils.get_snippet(_snippet_file)
            _content = ParserContent(
                ["$App$", "$app$", "$Model$", "$ModelClassCamelCase$", "$model$", "$ModelClass$", "$project$"],
                [
                    self._source_app.app_name,
                    self._source_app.app_name.lower(),
                    convert_to_camel_case(self._source_app.model_name),
                    convert_to_camel_case(self._source_app.model_name),
                    self._source_app.model_name.lower(),
                    self._source_app.model_name,
                    self.command.flutter_project,
                ],
                _snippet_content,
            ).replace()
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Ocorreu o erro: {error} ao executar o _build_detail_page do PagesBuilder", exit=True)

    def _build_index_page(self):
        try:
            _target_file = Path(f"{self._pages_target_path}/index.dart")
            _snippet_file = Path(f"{self._snippet_dir}/index_page.txt")
            if Utils.check_file_is_locked(_target_file):
                return
            _snippet_content = Utils.get_snippet(_snippet_file)
            content = ParserContent(
                ["$ModelClass$", "$ModelClassCamelCase$", "$project$"],
                [
                    self._source_app.model_name,
                    convert_to_camel_case(self._source_app.model_name),
                    self.command.flutter_project.lower(),
                ],
                _snippet_content,
            ).replace()

            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(content)
        except Exception as error:
            Utils.show_error(f"Ocorreu o erro: {error} ao executar o _build_index_page do PagesBuilder")

    def _build_list_page(self):
        try:
            _target_file = Path(f"{self._pages_target_path}/list.dart")
            _snippet_file = Path(f"{self._snippet_dir}/list_page.txt")
            if Utils.check_file_is_locked(_target_file):
                return
            _snippet_content = Utils.get_snippet(_snippet_file)
            content = ParserContent(
                [
                    "$App$",
                    "$Model$",
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                    "$project$",
                ],
                [
                    self._source_app.app_name,
                    self._source_app.model_name_lower,
                    self._source_app.model_name,
                    convert_to_camel_case(self._source_app.model_name),
                    self.command.flutter_project,
                ],
                _snippet_content,
            ).replace()

            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(content)
        except Exception as error:
            Utils.show_error(f"Ocorreu o erro: {error} ao executar o _build_list_page do PagesBuilder")
