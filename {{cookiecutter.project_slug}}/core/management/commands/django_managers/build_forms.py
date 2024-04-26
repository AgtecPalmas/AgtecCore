from ..utils import Utils


class FormsBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_root = self.command.path_root
        self.path_core = self.command.path_core
        self.snippet_form = (
            f"{self.path_core}/management/commands/snippets/django/forms/form.txt"
        )
        self.snippet_form_url = (
            f"{self.path_core}/management/commands/snippets/django/forms/form_urls.txt"
        )
        self.path_form = f"{self.command.path_form}/{self.command.model_lower}.py"
        self.path_root_form = self.command.path_form
        self.app = self.command.app
        self.model = self.command.model
        self.model_class = self.command.model_class

    def get_model(self):
        """Método responsável por retornar a instância da class da App"""
        try:
            return self.apps.get_model(self.app, self.model)
        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.get_model: {error}",
            )

    def __get_related_fields(self) -> list:
        """Método para retornar os campos relacionados do model"""
        try:
            model = self.get_model()
            fields = model._meta.fields

            related_fields = [
                field
                for field in fields
                if field.get_internal_type()
                in ["ForeignKey", "ManyToManyField", "OneToOneField"]
            ]

            return related_fields + list(model._meta.many_to_many)

        except Exception as error:
            Utils.show_error(f"Error in FormsBuild.__get_related_fields: {error}")

    @staticmethod
    def __add_widgets_meta(content: str, related_fields: list) -> str:
        """Método para adicionar os widgets no Meta do form"""
        try:
            widgets_meta = "".join(
                [
                    f'\t\t"{field.name}": {field.related_model.__name__}Widget,\n'
                    for field in related_fields
                ]
            )

            # add "widget" to class Meta or update if already exists
            if "class Meta:" in content:
                if "widgets = {" in content:
                    content = content.replace(
                        "widgets = {",
                        f"""
        widgets = {{
{widgets_meta}
        }}""",
                    )
                else:
                    content = content.replace(
                        "class Meta:",
                        f"""
    class Meta:
        widgets = {{
{widgets_meta}
        }}""",
                    )

            return content

        except Exception as error:
            Utils.show_error(f"Error in FormsBuild.__add_widgets_meta: {error}")

    def __build_select2_widget(self, content: str, related_fields: list) -> str:
        """Método para adicionar o widget de select2 no arquivo de form"""
        try:
            # Create Widgets
            created_widgets = []
            snippet = Utils.get_snippet(
                f"{self.path_core}/management/commands/snippets/django/forms/select2_widget.txt"
            )
            for field in related_fields:
                if (
                    Utils.check_content(
                        self.path_form,
                        f"class {field.related_model.__name__}Widget",
                    )
                    is True
                ):
                    continue

                if field.related_model.__name__ in created_widgets:
                    continue

                created_widgets.append(field.related_model.__name__)

                model_import = f"from {field.related_model.__module__} import {field.related_model.__name__}"

                widget_content = snippet
                widget_content = widget_content.replace(
                    "$ModelClass$", field.related_model.__name__
                ).replace("$Multiple$", "Multiple" if field.many_to_many else "")

                content = f"{model_import}\n{widget_content}\n{content}"

            content = self.__add_widgets_meta(content, related_fields)
            return content

        except Exception as error:
            Utils.show_error(f"Error in FormsBuild.__build_select2_widget: {error}")

    def __model_is_fk(self) -> bool:
        """Método para verificar se o model atual é FK em algum lugar"""
        try:
            for model in self.apps.get_models():
                for field in model._meta.fields:
                    if (
                        field.is_relation
                        and field.related_model
                        and field.related_model.__name__ == self.model
                    ):
                        return True
            return False
        except Exception as error:
            Utils.show_error(f"Erro em FormsBuild.__exists_fk: {error}")

    def __get_modal_form(self) -> str:
        return f"class {self.model}ModalForm({self.model}Form):..."

    def build(self):
        try:
            content = Utils.get_snippet(str(self.snippet_form))
            content = content.replace("$ModelClass$", self.model)

            content_urls = Utils.get_snippet(str(self.snippet_form_url))
            content_urls = content_urls.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$app$", self.app)

            model_is_fk = self.__model_is_fk()
            fk_class = f"{self.__get_modal_form()}\n" if model_is_fk else ""

            related_fields = self.__get_related_fields()

            if related_fields:
                content = self.__build_select2_widget(content, related_fields)

            if Utils.check_dir(self.path_root_form) is False:
                Utils.create_directory(self.path_root_form, True)

            # Arquivo vazio ou inexistente
            if Utils.check_file(self.path_form) is False:
                with open(self.path_form, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"{content_urls}\n{content}\n{fk_class}\n")
                Utils.show_message("Forms criados com sucesso")
                return

            if Utils.check_file_is_locked(self.path_form) is True:
                return

            if Utils.check_content(self.path_form, f"class {self.model}Form"):
                if model_is_fk and not Utils.check_content(
                    self.path_form, f"class {self.model}ModalForm"
                ):
                    with open(self.path_form, "a", encoding="utf-8") as form:
                        form.write(f"{fk_class}\n")
                    Utils.show_message("[cyan]Modal Forms[/] adicionados")

                Utils.show_message("[cyan]Forms[/] já existem")
                return

            new_import = f"from {self.app}.models import {self.model}"

            # Não há problema appendar se houver formatação de código no processo
            with open(self.path_form, "a", encoding="utf-8") as form:
                form.write(f"{new_import}\n{content_urls}\n{content}\n{fk_class}\n")

        except Exception as error:
            Utils.show_error(f"Erro ao criar os FormsBuild.build: {error}")
