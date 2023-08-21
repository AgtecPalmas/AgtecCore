import os
from pathlib import Path

from ..constants.fastapi import *
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

    def __get_field_django_type(self, field):
        return str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")

    def __check_django_type_in_fields_types(self, field):
        return field.__class__.__name__ in self._fields_types.keys()

    def __add_attr_null(self, field, attribute):
        if getattr(field, "null", None):
            attribute = f"Optional[{attribute}]"
        return attribute

    def __add_attr_default(self, field, attribute):
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
        if field.attname == "django_user_id":
                attribute == "int"

        if "_id" in str(field.attname):
            attribute = f"Optional[UUID]"

        return attribute

    def build(self):
        try:
            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/schema.txt")))
            content = content.replace("$ModelClass$", self.model)
            model = self.app_instance.get_model(self.model)
            fields = model._meta.fields
            result = ""

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
                    attribute = self._fields_types.get(item["django_type"]).get("schema")
                    field_name = item.get("name")
                    attribute = self.__add_attr_null(field, attribute)
                    attribute = self.__add_attr_default(field, attribute)

                    if item.get("django_type") in ["ForeignKey", "OneToOneField"]:

                        if str(field_name) == "django_user":
                            content = content.replace(
                                "$auth_import$",
                                "from authentication.schemas import User",
                            )
                            result += f"\t django_user_id: int\n"
                            continue

                        if "_id" in str(field_name):
                            result += f"\t {field_name}: Optional[UUID]\n"
                            continue

                        field_name = field.get_attname_column()[1]
                    result += f"\t {field_name}: {attribute}\n"

            # Many to Many
            for related_field in iter(model._meta.related_objects):
                if related_field.field.many_to_many:
                    attribute = "Set"
                    attribute = self.__add_attr_null(field, attribute)
                    attribute = self.__add_attr_default(field, attribute)
                    result += f"\t {related_field.field.name}: {attribute}\n"

            content = content.replace("$auth_import$", "")
            content = content.replace("$fields$", result)

            if Utils.check_file(self.path_schema) is False:
                with open(self.path_schema, "w") as arquivo:
                    arquivo.write(content)
                PythonFormatter(self.path_schema).format()
                Utils.show_message("[cyan]Schemas[/] criados com sucesso")
                return

            if Utils.check_content(self.path_schema, f"class {self.model}"):
                Utils.show_message("[cyan]Schemas[/] já existem")
                return

            with open(self.path_schema, "a") as schema:
                schema.write("\n")
                schema.write(content)
            PythonFormatter(self.path_schema).format()
            Utils.show_message("[cyan]Schemas[/] criados com sucesso")

        except Exception as e:
            Utils.show_message(f"Erro ao criar o Schema do model {self.model}. Erro: {e}")
