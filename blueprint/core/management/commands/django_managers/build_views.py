from pathlib import Path
from typing import Tuple, List

from ..utils import Utils


class ViewsBuild:
    def __init__(self, command, apps):
        # Apps Model
        self.command = command
        self.apps = apps
        self.app = self.command.app

        # Model
        self.model = self.command.model
        self.model_class = self.command.model_class
        self.model_lower = self.command.model_lower

        # Paths
        self.path_core = self.command.path_core
        self.snippets_dir = (
            f"{self.path_core}/management/commands/snippets/django/views"
        )
        self.templates_dir = f"{self.command.path_template_dir}"
        self.path_root_views: Path = Path(f"{self.command.path_views}")
        self.path_indexview: Path = Path(f"{self.path_root_views}/index.py")
        self.path_model_views: Path = Path(
            f"{self.path_root_views}/{self.model_lower}.py"
        )

        # Snippets
        self.snippet_index_view = f"{self.snippets_dir}/index_view.txt"
        self.snippet_crud_views = f"{self.snippets_dir}/crud_views.txt"
        self.snippet_cruds_urls = f"{self.snippets_dir}/crud_urls.txt"
        self.snippet_crud_modal_template = f"{self.snippets_dir}/crud_form_modal.txt"

    def get_verbose_name(self) -> str:
        """Método para retornar o verbose_name da app"""
        return (
            Utils.get_verbose_name(self.apps, app_name=self.app.lower())
            or self.app.lower()
        )


    def __build_index_view(self):
        __snippet_index_template = Utils.get_snippet(self.snippet_index_view)

        if (
            Utils.check_content(
                self.path_indexview,
                f"{self.app.title()}IndexTemplateView",
            )
            is False
        ):
            __snippet_index_template = __snippet_index_template.replace(
                "$AppClass$", self.app.title()
            )
            __snippet_index_template = __snippet_index_template.replace(
                "$app_name$", self.app.lower()
            )
            content = __snippet_index_template
            Utils.write_file(self.path_indexview, content)

    def __get_modal_forms(self) -> Tuple[str, List[str]]:
        """Método para retornar os forms modais do model atual"""
        _import_forms_modal = ""
        _forms = ""

        for fk_name in getattr(self.model_class._meta, "fk_fields_modal", []):
            _field = self.model_class._meta.get_field(fk_name)
            if not _field.related_model:
                Utils.show_error(
                    f"Modelo [cyan]{fk_name}[/] no fk_fields_modal não foi encontrado em [cyan]{self.model}[/]",
                    exit=False,
                )
                continue

            _app_name, _, _model_name = (
                str(_field.related_model).split("'")[1].split(".")
            )
            _import_forms_modal += f"\nfrom {_app_name}.forms.{_model_name.lower()} import {_model_name}ModalForm"
            _forms += f"{_model_name}ModalForm,"

        return _import_forms_modal, _forms

    def build(self):
        try:
            content = Utils.get_snippet(self.snippet_crud_views)
            content_urls = Utils.get_snippet(self.snippet_cruds_urls)

            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app_name$", self.app.lower())
            content = content.replace("$model_name$", self.model.lower())

            content_urls = content_urls.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$app_name$", self.app.lower())
            content_urls = content_urls.replace("$model_name$", self.model.lower())

            _import_forms_modal = ""

            if Utils.check_dir(self.path_root_views) is False:
                Utils.create_directory(self.path_root_views, True)

            self.__build_index_view()

            _import_forms_modal, _modal_forms = self.__get_modal_forms()
            if _modal_forms:
                content = content.replace(
                    "# form_modals = []", f"form_modals = [{_modal_forms}]"
                )

            if hasattr(self.model_class._meta, "fields_display") is True:
                sorted_fields = sorted(self.model_class._meta.fields_display)
                content = content.replace(
                    "$ListFields$", f"list_display = {sorted_fields}"
                ).replace("$SearchFields$", f"search_fields = {sorted_fields}")

            else:
                content = content.replace("$ListFields$", "")
                content = content.replace("$SearchFields$", "")

            if Utils.check_file(self.path_model_views) is False:
                with open(self.path_model_views, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"{content_urls}\n{_import_forms_modal}\n{content}")
                Utils.show_message("Views criadas com sucesso")
                return

            if Utils.check_content(
                self.path_model_views, f"class {self.model}ListView"
            ):
                Utils.show_message("[cyan]Views[/] já existem")
                return

            new_import = f"from {self.app}.models import {self.model}"

            with open(self.path_model_views, "a", encoding="utf-8") as views:
                views.write(
                    f"{new_import}\n{content_urls}\n{_import_forms_modal}\n{content}\n"
                )

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o ViewsBuild.build do models {self.model} | {error}",
            )
