from pathlib import Path

from ..constants.fastapi import *
from ..formatters import PythonFormatter
from ..utils import Utils


class ModelsBuild:
    def __init__(self, command):
        self.command = command
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.model.lower()
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/fastapi/")
        self.path_app = Path(f"{self.command.fastapi_dir}/{self.app}")
        self.path_model_fastapi = Path(f"{self.path_app}/{self.model_lower}/models.py")
        self.app_instance = self.command.app_instance
        self._fields_types = FIELDS_TYPES

    def __check_django_type_in_fields_types(self, field):
        return field in self._fields_types.keys()

    def __get_field_django_type(self, field):
        return str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")

    def __add_attr_default(self, field, attribute):
        if field.get_default() is not None and field.get_default() != "":
            f", default = {field.get_default()}"
            field_str = field.get_default()

            if attribute in ["int", "float", "bool"]:
                attribute += f", default = {field_str}"

            elif attribute == "datetime.date":
                year, month, day = [int(x) for x in field_str.split("-")]
                attribute += f", default = datetime.date({year}, {month}, {day})"

            elif attribute == "datetime.time":
                hour, minute, mili = [int(x) for x in field_str.split(":")]
                attribute += f", default = datetime.time({hour}, {minute}, {mili})"

            elif attribute == "datetime.datetime":
                date_split, hour_split = field_str.split(" ")
                year, month, day = [int(x) for x in date_split.split("-")]
                hour, minute, mili = [int(x) for x in hour_split.split(":")]
                attribute = f"DateTime, default = datetime.datetime({year}, {month}, {day}, {hour}, {minute}, {mili})"

            else:
                attribute += f", default = '{field_str}'"
        return attribute

    def build(self):
        try:
            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/model.txt")))
            content = content.replace("$ModelClass$", self.model)
            model = self.app_instance.get_model(self.model)
            content = content.replace("$table$", model._meta.db_table)
            fields = model._meta.fields
            related_fields = model._meta.many_to_many
            result = ""
            imports = ""
            many_to_many = ""
            for field in iter(fields):
                item = {
                    "app": (str(field).split("."))[0],
                    "model": (str(field).split("."))[1],
                    "name": (str(field).split("."))[2],
                    "django_type": self.__get_field_django_type(field),
                }

                if not self.__check_django_type_in_fields_types(item.get("django_type")):
                    Utils.show_error(f"Campo {item.get('django_type')} desconhecido.", exit=False)
                    continue

                if not Utils.check_ignore_field(item["name"]):
                    attribute = self._fields_types.get(item["django_type"]).get("model")
                    field_name = item.get("name")
                    relationship = None
                    if field.max_length:
                        attribute += f"({field.max_length})"
                    # Tratando campos do tipo ForeignKey ou OneToOneField
                    if item.get("django_type") in ["ForeignKey", "OneToOneField"]:
                        if item.get("name") == "django_user_id":
                            attribute = f"Integer"
                        else:
                            field_name = field.get_attname_column()[1]
                            __model = field.related_model._meta
                            attribute = f"ForeignKey('{__model.db_table}.id')"
                            if __model.app_label not in [item.get("app"), "auth"]:
                                imports += f"from {__model.app_label}.{__model.object_name.lower()}.models import {__model.object_name}\n"
                            if item.get("name") != "django_user":
                                relationship = f"\t{item.get('name')} = relationship('{__model.object_name}', foreign_keys=[{field_name}])\n"

                    attribute = f"{attribute}, nullable={(getattr(field, 'null', None))}"

                    if item.get("name") == "django_user":
                        mapped_field = "Integer"
                    else:
                        mapped_field = self._fields_types.get(item["django_type"]).get("model")

                    if field.has_default():
                        attribute = self.__add_attr_default(field, mapped_field)
                    if field.unique is True:
                        attribute += f" ,unique={field.unique}"
                    result += f"\t{field_name}: Mapped[{mapped_field}] = mapped_column({attribute})\n"
                    if relationship is not None:
                        result += relationship

            # Tratando campos do tipo ManyToManyField
            for related_field in iter(related_fields):
                related_item = {
                    "app": (str(related_field).split("."))[0],
                    "model": (str(related_field).split("."))[1],
                    "name": (str(related_field).split("."))[2],
                    "django_type": self.__get_field_django_type(related_field),
                }
                if related_item.get("django_type") == "ManyToManyField":
                    _model_name = related_field.model._meta.model_name
                    _app_name = related_field.model._meta.app_label
                    _related_model_name = related_field.related_model._meta.model_name
                    _related_model_app = related_field.related_model._meta.app_label
                    __model = related_field.related_model._meta
                    table = f"{related_item.get('app')}_{_model_name}_{related_item.get('name')}"
                    # Variável contendo o nome da tabela ManyToMany que é utilizado na tabela de ligação
                    table_related_name = f"{model._meta.db_table}_{related_item.get('name')}"
                    many_to_many += f'{table} = Table("{table_related_name}", CoreBase.metadata,'
                    many_to_many += "Column('id', Integer, primary_key=True, index=True),"

                    # Verificando se o relacionamento é com ele mesmo
                    if _model_name == _related_model_name and _app_name == _related_model_app:
                        many_to_many += (
                            f"Column('from_{_model_name}_id', ForeignKey('{model._meta.db_table}.id')),"
                        )
                        many_to_many += f"Column('to_{_related_model_name}_id', ForeignKey('{__model.db_table}.id')))\n"
                    else:
                        many_to_many += f"Column('{_model_name}_id', ForeignKey('{model._meta.db_table}.id')),"
                        many_to_many += f"Column('{_related_model_name}_id', ForeignKey('{__model.db_table}.id')))\n"

                    result += f'\t{related_item.get("name")}: Mapped[List["{__model.object_name}"]] = relationship(secondary={table}, backref="{table.replace("_", "")}", lazy="joined")\n'

            content = content.replace("$columns$", result)
            content = content.replace("$imports$", imports)
            content = content.replace("$manyToMany$", many_to_many)

            if Utils.check_file(self.path_model_fastapi) is False:
                with open(self.path_model_fastapi, "w") as arquivo:
                    arquivo.write(content)
                PythonFormatter(self.path_model_fastapi).format()
                Utils.show_message("[cyan]Models[/] criados com sucesso")
                return

            if Utils.check_content(self.path_model_fastapi, f"class {self.model}"):
                Utils.show_message("[cyan]Models[/] já existem")
                return

            with open(self.path_model_fastapi, "a") as schema:
                schema.write("\n")
                schema.write(content)
            PythonFormatter(self.path_model_fastapi).format()
            Utils.show_message("[cyan]Models[/] criados com sucesso")

        except Exception as error:
            Utils.show_error(f"Erro ao criar o arquivo model.py: {error}")
