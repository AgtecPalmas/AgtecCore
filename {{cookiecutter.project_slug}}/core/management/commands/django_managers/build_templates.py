import os
from pathlib import Path

from ..formatters import HtmlFormatter
from ..utils import Utils


class TemplatesBuild:
    def __init__(self, command, apps, force=False):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core
        self.snippets_dir = (
            f"{self.path_core}/management/commands/snippets/django/templates"
        )
        self.templates_dir = f"{self.command.path_template_dir}"
        self.app = self.command.app
        self.app_lower = self.command.app_lower
        self.model = self.command.model
        self.model_lower = self.command.model_lower
        self.force = force

        self.model_template_path = Path(f"{self.templates_dir}/{self.model_lower}")
        self.index_template = Path(f"{self.templates_dir}/index.html")
        self.detail_template = Path(
            f"{self.model_template_path}/{self.model_lower}_detail.html"
        )
        self.list_template = Path(
            f"{self.model_template_path}/{self.model_lower}_list.html"
        )
        self.create_template = Path(
            f"{self.model_template_path}/{self.model_lower}_create.html"
        )
        self.delete_template = Path(
            f"{self.model_template_path}/{self.model_lower}_delete.html"
        )
        self.update_template = Path(
            f"{self.model_template_path}/{self.model_lower}_update.html"
        )
        self.restore_template = Path(
            f"{self.model_template_path}/{self.model_lower}_restore.html"
        )

    def get_file_path(self, template_name: str) -> str:
        if template_name == "index":
            return f"{self.templates_dir}/index.html"
        return f"{self.model_template_path}/{self.model_lower}_{template_name}.html"

    def get_snippet_content(self, template_name: str) -> str:
        return Utils.get_snippet(str(Path(f"{self.snippets_dir}/{template_name}.txt")))

    def get_verbose_name(self) -> str:
        """Método para retornar o verbose_name da app"""
        return (
            Utils.get_verbose_name(self.apps, app_name=self.app_lower) or self.app_lower
        )

    def build(self):
        try:
            if Utils.check_dir(str(self.command.path_template_dir)) is False:
                os.makedirs(self.command.path_template_dir)
                Utils.show_message("Diretório de [cyan]templates[/] criado com sucesso")
            self.manage_index_template()
            self.manage_detail_template()
            self.manage_list_template()
            self.manage_create_template()
            self.manage_delete_template()
            self.manage_update_template()
            self.manage_restore_template()
            self.apply_formatters()

        except Exception as error:
            Utils.show_error(
                f"Erro ao criar os diretórios templates da app/models: {error}",
            )

    def apply_formatters(self):
        try:
            HtmlFormatter(self.index_template).format()
            HtmlFormatter(self.detail_template).format()
            HtmlFormatter(self.list_template).format()
            HtmlFormatter(self.create_template).format()
            HtmlFormatter(self.delete_template).format()
            HtmlFormatter(self.update_template).format()
            HtmlFormatter(self.restore_template).format()

        except Exception as error:
            Utils.show_error(f"Erro ao aplicar formatação HTML: {error}")

    def manage_index_template(self):
        try:
            path = self.get_file_path("index")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("index")
            _title = self.get_verbose_name()
            content = content.replace("$titlepage$", _title)
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("FileLocked", "#FileLocked")
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
                Utils.show_message("Template de [cyan]Index[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(f"Error in TemplatesBuild.manage_index_template: {error}")

    def manage_detail_template(self):
        try:
            path = self.get_file_path("detail")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("detail")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace(
                "$url_back$", f"{self.app_lower}:{self.model_lower}-list"
            ).replace("FileLocked", "#FileLocked")
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
                Utils.show_message("Template de [cyan]Detail[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_detail_template : {error}"
            )

    def manage_list_template(self):
        try:
            path = self.get_file_path("list")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("list")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$label_count_item$", self.model)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
                Utils.show_message("Template de [cyan]List[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_list_template : {error}",
            )

    def manage_create_template(self):
        try:
            path = self.get_file_path("create")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("create")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            content = content.replace("$model_name_lower$", self.model_lower)
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
                Utils.show_message("Template de [cyan]Criação[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_create_template : {error}"
            )

    def manage_update_template(self):
        try:
            path = self.get_file_path("update")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("update")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            content = content.replace("$model_name_lower$", self.model_lower)
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
                Utils.show_message(
                    "Template de [cyan]Atualização[/] criado com sucesso"
                )

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_update_template : {error}"
            )

    def manage_delete_template(self):
        try:
            path = self.get_file_path("delete")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("delete")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            content = content.replace("FileLocked", "#FileLocked")
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
            Utils.show_message("Template de [cyan]Deleção[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_delete_template : {error}"
            )

    def manage_restore_template(self):
        try:
            path = self.get_file_path("restore")
            if Utils.check_file_is_locked(str(path)) and not self.force:
                return
            content = self.get_snippet_content("restore")
            _title = self.get_verbose_name()
            content = content.replace("$title$", _title)
            content = content.replace("$app_name$", self.app_lower)
            content = content.replace("$model_name$", self.model_lower)
            content = content.replace("$app_title$", self.app.title())
            content = content.replace("$model_title$", self.model.title())
            content = content.replace("FileLocked", "#FileLocked")
            with open(path, "w", encoding="utf-8") as template:
                template.write(content)
            Utils.show_message("Template de [cyan]Restauração[/] criado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in TemplatesBuild.manage_restore_template : {error}"
            )
