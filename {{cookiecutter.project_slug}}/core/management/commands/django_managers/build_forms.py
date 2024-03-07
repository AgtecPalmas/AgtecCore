import os

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
