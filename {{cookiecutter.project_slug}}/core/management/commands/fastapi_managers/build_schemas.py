import os
from pathlib import Path

from ..constants.fastapi import FIELDS_TYPES
from ..formatters import PythonFormatter
from ..utils import Utils


class SchemasBuild:
    def __init__(self, command):
        self.command = command
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.model.lower()
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/fastapi/")
        self.path_app = os.path.join(self.command.fastapi_dir, self.app)
        self.path_schema: Path = Path(f"{self.path_app}/{self.model_lower}/schemas.py")
        self.app_instance = self.command.app_instance
        self._fields_types = FIELDS_TYPES

    def __get_field_django_type(self, field): # noqa
        return (
            str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")
        )

    def __check_django_type_in_fields_types(self, field):
        return field.__class__.__name__ in self._fields_types.keys()

    def __add_attr_null(self, field, attribute): # noqa
        if getattr(field, "null", None):
            attribute = f"Optional[{attribute}] = None"
        return attribute

    def __add_attr_default(self, field, attribute): # noqa
        if field.get_default() is not None and field.get_default() != "":
            field_str = field.get_default()

            if attribute in ["int", "float", "bool"]:
                attribute += f" = {field_str}"

            elif attribute == "datetime.date":
                year, month, day = [int(x) for x in field_str.split("-")]
                attribute += f" = datetime.date({year}, {month}, {day})"

            elif attribute == "datetime.time":
                hour, minute, mili = [int(x) for x in field_str.split(":")]
                attribute += f" = datetime.time({hour}, {minute}, {mili})"

            elif attribute == "datetime.datetime":
                date_split, hour_split = field_str.split(" ")
                year, month, day = [int(x) for x in date_split.split("-")]
                hour, minute, mili = [int(x) for x in hour_split.split(":")]
                attribute += f" = datetime.datetime({year}, {month}, {day}, {hour}, {minute}, {mili})"

            else:
                attribute += f" = '{field_str}'"

        return attribute

    def build(self):
        try:
            if Utils.check_content(self.path_schema, f"class {self.model}"): # noqa
                Utils.show_message("[cyan]Schemas[/] já existem") # noqa
                return

            model = self.app_instance.get_model(self.model)
            class_is_inherited = model.__bases__[0].__name__ != "Base"
            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/schema.txt")))
            if class_is_inherited is True:
                content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/schema_inherited.txt")))
            content = content.replace("$ModelClass$", self.model)
            fields = model._meta.fields # noqa
            result = ""
            fields_db = ""

            for field in iter(fields):
                item = {
                    "app": (str(field).split("."))[0],
                    "model": (str(field).split("."))[1],
                    "name": (str(field).split("."))[2],
                    "django_type": self.__get_field_django_type(field),
                }

                if not self.__check_django_type_in_fields_types(field):
                    Utils.show_error(f"Campo {field} desconhecido.", exit=False)
                    continue

                if not Utils.check_ignore_field(item["name"]):
                    attribute = self._fields_types.get(item["django_type"]).get(
                        "schema"
                    )
                    field_name = item.get("name")

                    if getattr(field, "swappable_setting", None) == "AUTH_USER_MODEL":
                        content = content.replace(
                            "$auth_import$",
                            "from authentication.schemas import User",
                        )
                        attribute = "int"

                    attribute = self.__add_attr_null(field, attribute)
                    attribute = self.__add_attr_default(field, attribute)

                    if item.get("django_type") in ["ForeignKey", "OneToOneField"]:
                        # Checando se a classe herda de outro models e é o django_user
                        # para não renderizar o campo
                        if class_is_inherited is True and field_name == 'django_user':
                            continue

                        if str(field_name).endswith("_id"):
                            result += f"\t{field_name}: Optional[UUID]\n"
                            continue

                        field_name = field.get_attname_column()[1]

                    # Checando se a classe herda de outro models
                    # para não renderizar os atributos do models Pai no Schema
                    if class_is_inherited is True:
                        _itens_classe = list(model.__dict__.keys())
                        if field_name in field_name in _itens_classe:
                            result += f"\t{field_name}: {attribute}\n"
                            # Filtrando apenas os campos do models mesmo, removendo o
                            # que termina com _ptr_id
                            if str(field_name).endswith('_ptr_id') is False:
                                fields_db += f"    {field_name}: {attribute}\n"
                    else:
                        result += f"\t{field_name}: {attribute}\n"

            # Many to Many
            for related_field in iter(model._meta.many_to_many): # noqa
                attribute = "Set"
                attribute = self.__add_attr_null(related_field, attribute)
                attribute = self.__add_attr_default(related_field, attribute)
                result += f"\t{related_field.name}: {attribute}\n"

            content = content.replace("$auth_import$", "")
            content = content.replace("$fields$", result)
            content = content.replace("$fields_db$", fields_db)

            if Utils.check_file(self.path_schema) is False: # noqa
                with open(self.path_schema, "w") as arquivo:
                    arquivo.write(content)

            else:
                with open(self.path_schema, "a") as schema:
                    schema.write("\n")
                    schema.write(content)

            PythonFormatter(self.path_schema).format() # noqa
            Utils.show_message("[cyan]Schemas[/] criados com sucesso") # noqa

        except Exception as e:
            Utils.show_message(
                f"Erro ao criar o Schema do model {self.model}. Erro: {e}" # noqa
            )
