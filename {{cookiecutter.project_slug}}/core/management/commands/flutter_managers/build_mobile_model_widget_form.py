"""
Build para gerenciar a criação dos arquivos da camanda de models
de cada model da App, que serão criados dentro do diretório
models

"""
from pathlib import Path

from core.management.commands.constants.flutter import (
    DJANGO_TYPES,
    FLUTTER_TYPES,
    IGNORE_FIELDS,
)
from core.management.commands.flutter_managers.utils import (
    convert_to_camel_case,
    ignore_base_fields,
)
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils


class AppsMobileWidgetFormBuilder:
    def __init__(self, command, app) -> None:
        
        self.command = command
        self.app = app
        self.flutter_dir = self.command.flutter_dir
        self.flutter_widget_form_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_mobile_project/layers/form.txt"
        )
        self.flutter_widget_form_field_snippet = Path(
            f"{self.command.path_command}/snippets/flutter_mobile_project/layers/textfield.txt"
        )
        self.form_attribute_value_to_model = ""
        self.list_form_attribute_value_to_model = []

    def build(self):
        try:
            # Pegando os models da app
            _models_app = self.app.get_models()
            for model in _models_app:
                _model_app = self.app.name
                _model_app_lower = _model_app.lower()
                _model_name = model.__name__
                _model_name_lower = _model_name.lower()
                _form_field_file_dart = Path(
                    f"{self.flutter_dir}/lib/apps/{_model_app_lower}/widgets/{_model_name_lower}.form.dart"
                )
                self.form_app = _form_field_file_dart
                self._build_form(model=model)

        except Exception as error:
            Utils.show_error(f"Error building models: {error}")
            raise error

    def _get_controllers_data(self, attribute, model_name, name, name_title) -> str:
        _controllers_data = ""
        _space = " " * 16
        _model_cc = convert_to_camel_case(model_name)
        _title = name_title
        try:
            if attribute == "int":
                if f"id{model_name.lower()}" == name.lower():
                    _controllers_data = f"{_space}_{_model_cc}Model.id = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
                else:
                    _controllers_data = f"{_space}_{_model_cc}Model.{name} = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"
            elif attribute == "double":
                _controllers_data = f"{_space}_{_model_cc}Model.{name} = double.tryParse(_{_model_cc}Form{_title}.text) ?? 0.0;\n"
            elif attribute == "bool":
                _field_is_empty = f"_{_model_cc}Form{_title}.text.isNotEmpty"
                _fields_contains_zero = (
                    f"_{_model_cc}Form{_title}.text.contains('0') ? true: false : false"
                )
                _controllers_data = f"{_space}_{_model_cc}Model.{name} = {_field_is_empty} ? {_fields_contains_zero};\n"
            elif attribute == "DateTime?":
                _controllers_data = f"{_space}_{_model_cc}Model.{name} = _{_model_cc}Form{_title}.text != ''?"
                _controllers_data += (
                    f" Util.convertDate(_{_model_cc}Form{_title}.text) : null;\n"
                )
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
                    _attribute = f"{_space}_{_model_cc}Model.{name} = int.tryParse(_{_model_cc}Form{_title}.text) ?? 0;\n"

            elif attribute == "double":
                _attribute = f"{_space}_{_model_cc}Model.{name} = double.tryParse(_{_model_cc}Form{_title}.text) ?? 0.0;\n"
            elif attribute == "bool":
                _check_field = f"_{_model_cc}Form{_title}.text.isNotEmpty"
                _i_contains = (
                    f"_{_model_cc}Form{_title}.text.contains('0') ? true: false : false"
                )
                _attribute = f"{_space}_{_model_cc}Model.{name} = {_check_field} ? {_i_contains};\n"
            elif attribute == "DateTime?":
                _convert = f"?Util.convertDate(_{_model_cc}Form{name_title}.text): null"
                _attribute = f"{_space}_{_model_cc}Model.{name} = "
                _attribute += f"_{_model_cc}Form{name_title}.text != '' {_convert};\n"
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
        
    def _check_field_ignore(self, field):
        """
        Método responsável por verificar se o campo é um dos campos
        que não devem ser exibidos no form
        """
        try:
            _lower_field = field.lower()
            _ignore_form_fields = IGNORE_FIELDS
            _ignore_form_fields += ("djangouser", "latitude", "longitude")
            return _lower_field in _ignore_form_fields
        except Exception as error:
            Utils.show_error(f"Error in _check_field_ignore: {error}")
            return True

    def _get_form_attribute_value_to_model(self, class_form):
        """
        Método responsável por renderizar a atribuição 
        dos valores dos controllers para o model 
        """
        _list_attribute = ""

        # Percorrendo o self.list_form_attribute_value_to_model para 
        for _attribute in self.list_form_attribute_value_to_model:
            _title_camel_case = convert_to_camel_case(
                str(_attribute.get("field"))
            )
            _textField = f"_{class_form}Form{str(_attribute.get('field'))}.text"
            if _attribute.get("type") == "double":
                _list_attribute += f"_{class_form}Model.{_title_camel_case} = double.tryParse({_textField}) ?? 0.0;\n"
                continue
            if _attribute.get("type") == "int":
                _list_attribute += f"_{class_form}Model.{_title_camel_case} = int.tryParse({_textField}) ?? 0;\n"
                continue
            if _attribute.get("type") == "DateTime?":
                _list_attribute += f"_{class_form}Model.{_title_camel_case} = AppConvertData.parseDataBrasileira({_textField}) ?? DateTime.now();\n"
                continue
            if _attribute.get("type") == "bool":
                _list_attribute += f"_{class_form}Model.{_title_camel_case} = bool.tryParse({_textField}) ?? false;\n"
                continue
            else:
                _list_attribute += f"_{class_form}Model.{_title_camel_case} = {_textField};\n"

        self.form_attribute_value_to_model = _list_attribute

    def _build_form(self, model):
        try:

            _form_content_file = self.flutter_widget_form_field_snippet
            if Utils.check_file_is_locked(str(self.form_app)):
                return
            _content_attributes = ""
            _content_attributes_update = ""
            _dispose_attributes = ""
            _text_fields = ""
            _attributes_data = ""
            _clear_data = ""
            _edited_attributes = ""
            _get_controllers_data = ""
            _snippet_content = Utils.get_snippet(self.flutter_widget_form_snippet)
            _content_form = Utils.get_snippet(_form_content_file)
            for field in iter(model._meta.fields):  # noqa W0212
                _, __, _name = str(field).split(".")
                _name_title = self._to_camel_case(_name.title())
                _name = self._to_camel_case(_name.lower())

                if ignore_base_fields(_name):
                    continue

                field_type = (
                    str(str(type(field)).split(".")[-1:])
                    .replace('["', "")
                    .replace("'>\"]", "")
                )

                attribute = FLUTTER_TYPES[DJANGO_TYPES.index(field_type)]
                _model_name = model.__name__
                _model_name_camel_case = convert_to_camel_case(
                    _model_name
                )

                # Dando um ByPass para os campos que não devem ser exibidos no form
                if self._check_field_ignore(_name):
                    continue

                _content_attributes += f"  final _{_model_name_camel_case}Form{_name_title} = TextEditingController();\n"
                
                # Adicionando o content_attributes_update para quando estiver editando
                # Verificando se o campo é do tipo DateField ou DateTimeField
                if field_type in ["DateField", "DateTimeField"]:
                    _content_attributes_update += (
                        f"  _{_model_name_camel_case}Form{_name_title}.text = "
                        f"DateFormat('dd/MM/yyyy').format(_{_model_name_camel_case}Model.{_name}!);\n"
                    )
                else:
                    _content_attributes_update += f"_{_model_name_camel_case}Form{_name_title}.text = _{_model_name_camel_case}Model.{_name}.toString();\n"

                _dispose_attributes += (
                    f"    _{_model_name_camel_case}Form{_name_title}.dispose();\n"
                )
                text_field = _content_form
                controller = f"_{_model_name_camel_case}Form{_name_title}"
                text_field = text_field.replace("$controller$", controller)
                text_field = text_field.replace(
                    "$Field$", str(field.verbose_name).replace("R$", "R\$")
                )

                try:
                    _validator_less = ""
                    
                    # Verificando se o campo é required
                    _required_field = (
                        "required"
                        if getattr(field, "blank", None) is False
                        and getattr(field, "null", None) is False
                        else ""
                    )
                    if _required_field == "required":
                        _validator_less = "Validatorless.required('Campo obrigatório'),"
                    
                    # Criando o validator para o tamanho
                    _max_length_field = field.max_length
                    if _max_length_field is not None:
                        _validator_less += f"\n Validatorless.max({_max_length_field}, 'Máximo de {_max_length_field} caracteres'),"
                    
                    text_field = text_field.replace(
                        "$validators$", _validator_less
                    )
                except Exception as error:
                    Utils.show_error(
                        f"Error in _build_form: {error}", exit=False
                    )

                if field_type == "DateField" or field_type == "DateTimeField":
                    text_field = text_field.replace(
                        "$ImputFormatter$", 
                        "inputFormatters: [FilteringTextInputFormatter.digitsOnly, DataInputFormatter()],"
                    )

                if field_type == "DecimalField":
                    text_field = text_field.replace(
                        "$ImputFormatter$",
                        "inputFormatters: [FilteringTextInputFormatter.digitsOnly, RealInputFormatter(moeda: true)],"
                    )

                if "cpf" in _name.lower() or "cnpj" in _name.lower():
                    if "cpf" in _name.lower() and "cnpj" not in _name.lower():
                        text_field = text_field.replace(
                            "$ImputFormatter$",
                            "inputFormatters: [FilteringTextInputFormatter.digitsOnly, CpfInputFormatter()],"
                        )
                    elif "cnpj" in _name.lower() and "cpf" not in _name.lower():
                        text_field = text_field.replace(
                            "$ImputFormatter$",
                            "inputFormatters: [FilteringTextInputFormatter.digitsOnly, CnpjInputFormatter()],"
                        )
                    else:
                        text_field = text_field.replace(
                            "$ImputFormatter$",
                            "inputFormatters: [FilteringTextInputFormatter.digitsOnly, CpfOuCnpjFormatter()],"
                        )
                
                if "telefone" in _name.lower():
                    text_field = text_field.replace(
                        "$ImputFormatter$",
                        "inputFormatters: [FilteringTextInputFormatter.digitsOnly, TelefoneInputFormatter()],"
                    )

                #  Caso não seja nenhum dos casos acima, remover o inputFormatter
                text_field = text_field.replace("$ImputFormatter$", "")

                _text_fields += text_field
                _attributes_data += self._get_attributes_data(
                    attribute, _model_name, _name, _name_title
                )
                _get_controllers_data += self._get_controllers_data(
                    attribute, _model_name, _name, _name_title
                )
                _clear_data += f"    {controller}.clear();\n"

                if _name.startswith(f"id{_model_name.lower()}"):
                    _name = "id"

                _edited_attributes += f"      {controller}.text = _{_model_name_camel_case}Model.{_name}.toString();\n"

                # Apensando no list_form_attribute_value_to_model um dicionário contendo o nome do campo e o tipo
                self.list_form_attribute_value_to_model.append(
                    {"field": _name_title, "type": attribute}
                )

            self._get_form_attribute_value_to_model(convert_to_camel_case(model.__name__))

            content = ParserContent(
                [
                    "$ModelClass$",
                    "$Model$",
                    "$Attributes$",
                    "$AttributesUpdate$",
                    "$DisposeController$",
                    "$ClearData$",
                    "$Form$",
                    "$ModelLower$",
                    "$FormAttributeValueToModel$",
                ],
                [
                    _model_name,
                    convert_to_camel_case(model.__name__),
                    _content_attributes,
                    _content_attributes_update,
                    _dispose_attributes,
                    _clear_data,
                    _text_fields,
                    model.__name__.lower(),
                    self.form_attribute_value_to_model,
                ],
                _snippet_content,
            ).replace()

            with open(self.form_app, "w", encoding="utf-8") as _file:
                _file.write(content)

            # Limpando o self.list_form_attribute_value_to_model
            self.list_form_attribute_value_to_model = []
        except Exception as error:
            Utils.show_error(
                f"Ocorreu o erro: {error} ao executar o _build_form"
            )
