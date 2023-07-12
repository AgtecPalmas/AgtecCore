from ..utils import Utils
from pathlib import Path


class ViewsBuild:
    def __init__(self, command, apps):
        # Apps Model
        self.command = command
        self.apps = apps
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.command.model_lower

        # Paths
        self.path_core = self.command.path_core
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django"
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

    def get_model(self):
        """Método responsável por retornar a instância da class da App"""
        try:
            return self.apps.get_model(self.app, self.model)
        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.get_model: {error}",
            )

    @staticmethod
    def __get_models_from_content_urls(content: str) -> str:
        content = content.split("from ")
        models = []

        for item in content:
            if item.startswith(".models"):
                item = item.split("import ")[1]
                models.extend(model.strip() for model in item.split(","))
        return models

    @staticmethod
    def __get_forms_from_content_urls(content: str) -> str:
        content = content.split("from ")
        forms = []

        for item in content:
            if item.startswith(".forms"):
                item = item.split("import ")[1]
                forms.extend(form.strip() for form in item.split(","))
        return forms

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

    def build_init_file(self):
        """Método responsável por criar o arquivo __init__.py na pasta views"""
        content = "".join(
            f"from .{file.name.split('.')[0]} import *\n"
            for file in self.path_root_views.iterdir()
            if file.name not in ["__init__.py", "__pycache__"]
        )
        Utils.write_file(self.path_root_views / "__init__.py", content)

    def build(self):
        try:
            content = Utils.get_snippet(self.snippet_crud_views)
            content_urls = Utils.get_snippet(self.snippet_cruds_urls)
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app_name$", self.app.lower())
            content = content.replace("$model_name$", self.model.lower())
            content_urls = content_urls.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$app_name$", self.app.lower())
            _import_forms_modal = ""
            _model = self.get_model()

            if Utils.check_dir(self.path_root_views) is False:
                Utils.create_directory(self.path_root_views)

            self.__build_index_view()

            if hasattr(_model._meta, "fk_fields_modal") is True:
                _forms = ""
                for fk_name in _model._meta.fk_fields_modal:
                    _field = _model._meta.get_field(fk_name)
                    if not _field.related_model:
                        Utils.show_error(
                            f"Modelo [cyan]{fk_name}[/] no fk_fields_modal não foi encontrado em [cyan]{self.model}[/]",
                            exit=False,
                        )
                        continue
                    _field_name = str(_field.related_model).split("'")[1]
                    _field_split = _field_name.split(".")
                    _app_field = _field_split[0]
                    _model_field = _field_split[2]
                    _import_forms_modal += (
                        f"\nfrom {_app_field}.forms import {_model_field}Form"
                    )
                    _forms += "{s}context['form_{l}'] = {u}Form\n".format(
                        l=_model_field.lower(), u=_model_field, s=" " * 8
                    )
                modal_update = Utils.get_snippet(self.snippet_crud_modal_template)
                modal_update = modal_update.replace(
                    "$ModelClass$", f"{self.model}UpdateView"
                )
                modal_update = modal_update.replace("$FormsModal$", _forms.strip())
                content = content.replace("$FormsModalUpdate$", modal_update)

                modal_create = Utils.get_snippet(self.snippet_crud_modal_template)
                modal_create = modal_create.replace(
                    "$ModelClass$", f"{self.model}CreateView"
                )
                modal_create = modal_create.replace("$FormsModal$", _forms.strip())
                content = content.replace("$FormsModalCreate$", modal_create)

            else:
                content = content.replace("$FormsModalCreate$", "")
                content = content.replace("$FormsModalUpdate$", "")

            if hasattr(_model._meta, "fields_display") is True:
                content = content.replace(
                    "$ListFields$", f"list_display = {_model._meta.fields_display}"
                )

            else:
                content = content.replace("$ListFields$", "")

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

            if Utils.check_content(self.path_model_views, "from core.views"):
                content_models = self.__get_models_from_content_urls(content_urls)
                content_forms = self.__get_forms_from_content_urls(content_urls)

                with open(self.path_model_views, "r", encoding="utf-8") as arquivo:
                    data = []

                    for line in arquivo:
                        if line.startswith("from .models import"):
                            models = line.split("import")[-1].rstrip()
                            import_model = ", ".join(content_models)
                            models += f", {import_model}"
                            line = f"from .models import{models}\n"

                        elif line.startswith("from .forms import"):
                            forms = line.split("import")[-1].rstrip()
                            import_form = ", ".join(content_forms)
                            forms += f", {import_form}"
                            line = f"from .forms import{forms}\n"

                        data.append(line)
                    data.append(_import_forms_modal)
                with open(self.path_model_views, "w", encoding="utf-8") as arquivo:
                    arquivo.writelines(data)
            else:
                with open(self.path_model_views, "a", encoding="utf-8") as views:
                    views.write(content_urls)

            with open(self.path_model_views, "a", encoding="utf-8") as views:
                views.write(_import_forms_modal)
                views.write("\n")
                views.write(content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o ViewsBuild.build do models {self.model} | {error}",
            )
