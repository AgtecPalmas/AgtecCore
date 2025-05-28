import subprocess
from pathlib import Path
from string import Template

from django.db.models import Model
from django.db.models.fields import Field
from django.urls import NoReverseMatch, resolve, reverse

from core.management.commands.constants.django import INPUT_TYPES
from core.management.commands.formatters import HtmlFormatter
from core.management.commands.utils import Utils


class CustomDjangoField:
    def __init__(self, field: Field):
        self.app, self.model, self.name = str(field).split(".")
        self.tipo = field.get_internal_type()

    def is_tipo(self, tipo):
        return self.tipo == tipo


class ParserHTMLBuild:
    def __init__(self, command, apps):
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
        self.force = self.command.force_templates
        self.parser_only: bool = self.command.options.get("parserhtml", False)

        self.model_template_path = Path(f"{self.templates_dir}/{self.model_lower}")
        self.template_update = Path(
            f"{self.templates_dir}/{self.model_lower}_update.html"
        )
        self.template_create = Path(
            f"{self.templates_dir}/{self.model_lower}_create.html"
        )
        self.template_list = Path(f"{self.templates_dir}/{self.model_lower}_list.html")

    def get_verbose_name(self) -> str:
        """Método para retornar o verbose_name da app"""
        return (
            Utils.get_verbose_name(self.apps, app_name=self.app_lower) or self.app_lower
        )

    def get_model(self) -> Model:
        """Método responsável por retornar a instância da class da App"""
        try:
            return self.apps.get_model(self.app, self.model)

        except Exception as error:
            Utils.show_error(f"Error in RenderTemplatesBuid.get_model: {error}")

    def render_modal_foreign_key(self, model, app, model_lower, field_name):
        """Método responsável por renderizar os modais de foreignkey"""
        try:
            content = Utils.get_snippet(Path(f"{self.snippets_dir}/modal_form.txt"))
            content = content.replace("$ModelName$", model)
            content = content.replace("$app_name$", app)
            content = content.replace("$model_name$", model_lower)
            content = content.replace("$field_name$", field_name)
            return content

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.render_modal_foreign_key: {error}",
            )

    @staticmethod
    def __render_boolean_field_switch(html: str, field_name: str) -> str:
        """Método responsável por renderizar o switch do boolean field
        O retorno deve seguir o modelo abaixo:
        <div class="form-check col-md-6 mb-3">
            <div class="br-switch icon top mr-5">
            {{ form.campo }}
            {{ form.campo.label_tag }}
            {% if form.campo.errors %}
                {{ form.campo.errors }}
            {% endif %}
        </div>
        """
        try:
            boolean_field_switch = Template(
                """{% if form.$field_name in form.visible_fields %}\n\
                    <div class="form-check col-md-6 mb-3">\n\
                        <div class="br-switch icon top mr-5">\n\
                            {{ form.$field_name }}\n\
                            {{ form.$field_name.label_tag }}\n\
                            {% if form.$field_name.errors %}\n\
                                {{ form.$field_name.errors }}\n\
                            {% endif %}\n\
                        </div>\n\
                        $help_text\n\
                    </div>\n\
                {% endif %}"""
            )

            return html + boolean_field_switch.substitute(
                field_name=field_name,
                help_text=ParserHTMLBuild.__render_help_text("", field_name),
            )

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.render_boolean_field_switch: {error}",
            )

    @staticmethod
    def __render_help_text(html: str, field_name: str) -> str:
        """Método responsável por renderizar o help_text"""
        try:
            help_text = Template(
                """{% if form.$field_name.help_text %}\
                    <small class="form-text text-muted">\
                        {{ form.$field_name.help_text }}\
                    </small>\
                {% endif %}"""
            )
            return f"{html}\n{help_text.substitute(field_name=field_name)}"

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__render_help_text: {error}",
            )

    @staticmethod
    def __render_invalid_feedback(html: str, field_name: str) -> str:
        """Método responsável por renderizar o invalid_feedback"""
        try:
            if "invalid-feedback" in html:
                return html

            invalid_feedback = Template(
                """<div class="invalid-feedback">\
                        {{ form.$field_name.errors }}\
                </div>"""
            )
            return f"{html}\n{invalid_feedback.substitute(field_name=field_name)}"

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__render_invalid_feedback: {error}",
            )

    def __render_foreign_key_field(
        self, html: str, custom_field: CustomDjangoField, field: Field
    ) -> str:
        """Método responsável por renderizar o campo ForeignKey e OneToOneField"""

        try:
            foreign_key_template = Template(
                """<div class="input-group">\
                    {{ form.${field_name} }}\
                    {% if form.${field_name}.field.queryset.model|has_add_permission:request %}\
                        <span class="input-group-text btn btn-light" type="button" data-bs-toggle="modal"\
                            title="Adicionar ${model}"\
                            data-bs-target="#form_${field_name}_modal">\
                            <i class="fas fa-plus"></i>\
                        </span>\
                    {% endif %}\
                    <div class="invalid-feedback">\
                        {{ form.$field_name.errors }}\
                    </div>
                </div>"""
            )

            self.html_modals += self.render_modal_foreign_key(
                field.related_model._meta.object_name,
                field.related_model._meta.app_label,
                field.related_model._meta.model_name,
                custom_field.name,
            )

            return html + foreign_key_template.substitute(
                field_name=custom_field.name, model=custom_field.model
            )

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__render_foreign_key_field: {error}",
            )

    def render_input(self, field: Field):
        """Método responsável por renderizar os inputs do form"""
        try:
            _model = self.get_model()

            campo = CustomDjangoField(field)

            if campo.tipo not in INPUT_TYPES:
                Utils.show_message(
                    f"Campo {field} desconhecido, favor verificar o tipo do campo.",
                    emoji="warning",
                )
                return

            if campo.is_tipo("BooleanField"):
                return self.__render_boolean_field_switch("", campo.name)

            tag_result = '<div class="form-group col-md-6">'
            required = (
                "required"
                if getattr(field, "blank", None) is False
                and getattr(field, "null", None) is False
                else ""
            )

            label = "{{{{ form.{}.label_tag }}}}".format(campo.name)

            if not required:
                label += '<span class="text-muted ml-1">(Opcional)</span>'

            if (campo.is_tipo("ForeignKey") or campo.is_tipo("OneToOneField")) and (
                field.name in getattr(_model._meta, "fk_fields_modal", [])
            ):
                tag_result = self.__render_foreign_key_field(
                    tag_result + label, campo, field
                )

            else:
                tag_result += "{}\n{{{{ form.{} }}}}".format(label, campo.name)

            tag_result = self.__render_help_text(tag_result, campo.name)
            tag_result = self.__render_invalid_feedback(tag_result, campo.name)

            return f"{{% if form.{field.name} in form.visible_fields %}}{tag_result}</div>{{% endif %}}\n"

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.render_input: {error}",
            )

    def manage_create_and_update_templates(self, model):
        """Método para gerenciar os templates de criação e atualização"""
        try:
            self.html_modals = ""
            __fields = model._meta.fields + model._meta.many_to_many

            html_tag = "".join(
                self.render_input(field)
                for field in iter(__fields)
                if str(field).split(".")[2]
                not in (
                    "updated_at",
                    "created_at",
                    "deleted",
                    "enabled",
                    "id",
                )
            )

            if not html_tag:
                Utils.show_error(
                    "Nenhum campo foi encontrado para ser renderizado",
                    emoji="warning",
                )

            for template_type in ["create", "update"]:
                template = Path(
                    f"{self.model_template_path}/{self.model_lower}_{template_type}.html"
                )

                if Utils.check_file_is_locked(str(template)) is True and not self.force:
                    continue

                with open(template, "r", encoding="utf-8") as file:
                    content = file.read()

                content = (
                    content.replace(
                        "<!--REPLACE_PARSER_HTML-->",
                        html_tag,
                    )
                    .replace(
                        "<!--REPLACE_MODAL_HTML-->",
                        self.html_modals,
                    )
                    .replace(
                        "$url_back$",
                        f"{self.app_lower}:{self.model_lower}-list",
                    )
                    .replace(
                        "FileLocked",
                        "#FileLocked",
                    )
                )

                with open(template, "w", encoding="utf-8") as file:
                    file.write(content)

                Utils.show_message(
                    f"Template [cyan]{template_type}[/] parseado com sucesso"
                )

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.manage_create_update_templates: {error}",
            )

    def __render_list_boolean(self, field_name: str) -> str:
        """Método responsável por renderizar o boolean field na listagem"""
        boolean = Template(
            """<td>
                <span class="badge badge-{{ item.$field_name|yesno:'success,danger' }}">
                    {{ item.$field_name|yesno:'Sim,Não' }}
                </span>
            </td>"""
        )
        return boolean.substitute(field_name=field_name)

    def get_reverse_url(self, list_view):
        """Método para coletar a URL reversa"""
        # Tenta coletar a URL,
        # caso não consiga, executa uma nova instância do manage.py com o parserhtml
        try:
            return reverse(list_view)

        except NoReverseMatch:
            if self.parser_only is False:
                self.__thread_parserhtml()
                return
            else:
                Utils.show_error(
                    f"Error in RenderTemplatesBuid.build ao pegar o Reverse de {list_view}\
                    \nVerifique se as URLs estão corretas e execute novamente",
                )

        except Exception as reverse_url_error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.build ao pegar o Reverse: {reverse_url_error}",
            )

    def manage_list_template(self, model):
        try:
            if (
                Utils.check_file_is_locked(
                    f"{self.model_template_path}/{self.model_lower}_list.html"
                )
                and not self.force
            ):
                return

            list_view = f"{self.app_lower}:{self.model_lower}-list"

            reverse_url = self.get_reverse_url(list_view)
            if reverse_url is None:
                return

            fields_display = resolve(reverse_url).func.view_class.list_display
            thead, tline = "", ""
            for item in fields_display:
                app_field = next(
                    (
                        item_field
                        for item_field in model._meta.fields
                        if item == item_field.name
                    ),
                    None,
                )

                if app_field is None:
                    continue

                field_name = (
                    app_field.verbose_name.title()
                    if app_field.verbose_name
                    else "Não Definido."
                )
                thead += f"<th>{field_name}</th>\n"

                if app_field.get_internal_type() == "BooleanField":
                    tline += self.__render_list_boolean(item)

                else:
                    tline += "<td>{{{{ item.{} }}}}</td>\n".format(
                        item.replace("__", ".")
                    )

            list_template = Path(
                f"{self.model_template_path}/{self.model_lower}_list.html"
            )
            list_template_content = (
                Utils.get_snippet(list_template)
                .replace("<!--REPLACE_THEAD-->", thead)
                .replace("<!--REPLACE_TLINE-->", tline)
                .replace("FileLocked", "#FileLocked")
            )

            with open(list_template, "w", encoding="utf-8") as list_file:
                list_file.write(list_template_content)

            Utils.show_message("Template [cyan]List[/] parseado com sucesso")

        except Exception as error:
            Utils.show_error(
                f"Error in __manage_render_html ao realizar o parser do template : {error}",
            )

    def __apply_formatters(self):
        """Método para aplicar os formatters nos templates"""
        try:
            HtmlFormatter(self.template_create).format()
            HtmlFormatter(self.template_update).format()
            HtmlFormatter(self.template_list).format()

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__apply_formatters: {error}",
            )

    def build(self):
        """Método para construir os templates"""
        try:
            model = self.get_model()
            if model is None:
                Utils.show_error("Favor declarar a app no settings", emoji="warning")

            self.manage_create_and_update_templates(model)
            self.manage_list_template(model)
            self.__apply_formatters()

        except Exception as error:
            Utils.show_error(f"Error in RenderTemplatesBuid.build: {error}")

    def __thread_parserhtml(self):
        """Método para executar o parserhtml em uma thread
        devido o Base URL ainda não possuir as URLs do projeto
        na primeira execução da flag --all"""

        try:
            Utils.show_message("[cyan]Thread ParserHTML[/] executada com sucesso")
            subprocess.run(
                f"python manage.py build {self.app} {self.model} --parserhtml",
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
            )
        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__thread_parserhtml: {error}",
            )
