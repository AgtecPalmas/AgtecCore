import fileinput
import subprocess
from pathlib import Path
from string import Template

from bs4 import BeautifulSoup
from django.conf import settings
from django.db.models.fields import Field
from django.urls import NoReverseMatch, resolve, reverse

from ..constants.django import INPUT_TYPES
from ..formatters import HtmlFormatter
from ..utils import Utils


class DjangoField:
    def __init__(self, field: Field):
        self.app, self.model, self.name = str(field).split(".")
        self.tipo = self.get_tipo(field)

    @staticmethod
    def get_tipo(field: Field) -> str:
        try:
            return (
                str(str(type(field)).split(".")[-1:])
                .replace('["', "")
                .replace("'>\"]", "")
            )
        except Exception as error:
            Utils.show_error(
                f"Error in DjangoField.get_tipo: {error}",
            )

    def is_tipo(self, tipo):
        return self.tipo == tipo


class ParserHTMLBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django"
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

    def get_file_path(self, template_name: str) -> str:
        if template_name == "index":
            return f"{self.templates_dir}/index.html"

        if template_name == "detail":
            return f"{self.model_template_path}/{self.model_lower}_detail.html"

        if template_name == "list":
            return f"{self.model_template_path}/{self.model_lower}_list.html"

        if template_name == "create":
            return f"{self.model_template_path}/{self.model_lower}_create.html"

        if template_name == "delete":
            return f"{self.model_template_path}/{self.model_lower}_delete.html"

        if template_name == "update":
            return f"{self.model_template_path}/{self.model_lower}_update.html"

    def get_snippet_content(self, template_name: str) -> str:
        if template_name == "index":
            return Utils.get_snippet(
                str(Path(f"{self.snippets_dir}/indextemplate.txt"))
            )

        if template_name == "detail":
            return Utils.get_snippet(
                str(Path(f"{self.snippets_dir}/detailtemplate.txt"))
            )

        if template_name == "list":
            return Utils.get_snippet(str(Path(f"{self.snippets_dir}/listtemplate.txt")))

        if template_name == "create":
            return Utils.get_snippet(
                str(Path(f"{self.snippets_dir}/createtemplate.txt"))
            )

        if template_name == "update":
            return Utils.get_snippet(
                str(Path(f"{self.snippets_dir}/updatetemplate.txt"))
            )

        if template_name == "delete":
            return Utils.get_snippet(
                str(Path(f"{self.snippets_dir}/deletetemplate.txt"))
            )

    def get_verbose_name(self) -> str:
        """Método para retornar o verbose_name da app"""
        return (
            Utils.get_verbose_name(self.apps, app_name=self.app_lower) or self.app_lower
        )

    def get_model(self):
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
            <div class="invalid-feedback">
                Campo Requerido.
            </div>
            {% if form.campo.errors %}
                {{ form.campo.errors }}
            {% endif %}
        </div>
        """
        try:
            boolean_field_switch = Template(
                "{% if form.$field_name in form.visible_fields %}\n\
                    <div class='form-check col-md-6 mb-3'>\n\
                        <div class='br-switch icon top mr-5'>\n\
                            {{ form.$field_name }}\n\
                            {{ form.$field_name.label_tag }}\n\
                            <div class='invalid-feedback'>Campo Requerido.</div>\n\
                            {% if form.$field_name.errors %}\n\
                                {{ form.$field_name.errors }}\n\
                            {% endif %}\n\
                        </div>\n\
                        $help_text\n\
                    </div>\n\
                {% endif %}"
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
                "{% if form.$field_name.help_text %}\
                    <small class='form-text text-muted'>\
                        {{ form.$field_name.help_text }}\
                    </small>\
                {% endif %}"
            )
            return f"{html}\n{help_text.substitute(field_name=field_name)}"

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.__render_help_text: {error}",
            )

    def render_input(self, field: Field):
        """Método responsável por renderizar os inputs do form"""
        try:
            _model = self.get_model()

            campo = DjangoField(field)

            if campo.tipo in INPUT_TYPES:
                # Verificando se foi setado na constantes BOOLEAN_FIELD_IS_SWITCH
                if settings.BOOLEAN_FIELD_IS_SWITCH is True and campo.is_tipo(
                    "BooleanField"
                ):
                    return self.__render_boolean_field_switch("", campo.name)

                if campo.is_tipo("BooleanField"):
                    tag_result = "<div class='form-check col-md-6'>"

                else:
                    tag_result = "<div class='form-group col-md-6'>"

                required = "required"

                if (getattr(field, "blank", None) is True) or (
                    getattr(field, "null", None) is True
                ):
                    required = ""

                readonly = getattr(field, "readonly", "")
                label = "{{{{ form.{}.label_tag }}}}".format(campo.name)

                if campo.is_tipo("ForeignKey") or campo.is_tipo("OneToOneField"):
                    tag_result += label
                    _foreign_key_field = "\n{{{{ form.{} }}}}".format(campo.name)

                    if hasattr(_model._meta, "fk_fields_modal") is True:
                        if campo.name in _model._meta.fk_fields_modal:
                            _foreign_key_field = '\n<div class="input-group">'
                            _foreign_key_field += "{{{{ form.{} }}}}\n".format(
                                campo.name
                            )
                            _foreign_key_field += (
                                "{{% if form.{0}.field.queryset.model|{1} %}}".format(
                                    campo.name, "has_add_permission:request"
                                )
                            )
                            _foreign_key_field += '<button type="button" class="btn btn-outline-secondary"'
                            _foreign_key_field += (
                                ' data-bs-toggle="modal" data-bs-target='
                            )
                            _foreign_key_field += '"#form{}Modal"><i class="fas fa-plus"></i></button>{{% endif %}}'.format(
                                field.related_model._meta.object_name
                            )
                            _foreign_key_field += "</div>"
                            self.html_modals += self.render_modal_foreign_key(
                                field.related_model._meta.object_name,
                                campo.app,
                                field.related_model._meta.model_name,
                                campo.name,
                            )

                    tag_result += _foreign_key_field

                elif campo.is_tipo("BooleanField"):
                    tag_result += "{{{{ form.{} }}}}\n{}".format(campo.name, label)

                elif campo.is_tipo("ManyToManyField"):
                    tag_result += "{}\n{{{{ form.{} }}}}".format(label, campo.name)

                else:
                    tag_result += "{}\n{{{{ form.{} }}}}".format(label, campo.name)

                if readonly != "":
                    tag_result = tag_result.replace(
                        "class='", "class='form-control-plaintext "
                    )

                if required != "":
                    tag_result += (
                        '\n<div class="invalid-feedback">Campo Requerido.</div>'
                    )

                tag_result = self.__render_help_text(tag_result, campo.name)

                error_template = Template(
                    """<div class="invalid-feedback">
                            {{ form.$field_name.errors }}
                        </div>"""
                )

                tag_result += error_template.substitute(field_name=campo.name)
                tag_result += "</div>"

                # Adicionando o teste para verificar se o campo está oculto no init do Form
                tag_result = f"{{% if form.{field.name} in form.visible_fields %}}{tag_result}{{% endif %}}\n\t"
                return tag_result

            else:
                Utils.show_message(
                    f"⚠️ Campo {field} desconhecido, favor verificar o tipo do campo."
                )

        except Exception as error:
            Utils.show_error(
                f"Error in RenderTemplatesBuid.render_input: {error}",
            )

    def manage_create_update_templates(self, model):
        """Método para gerenciar os templates de criação e atualização"""
        try:
            self.html_modals = ""
            __fields = model._meta.fields + model._meta.many_to_many

            html_tag = "".join(
                self.render_input(field)
                for field in iter(__fields)
                if str(field).split(".")[2]
                not in (
                    "updated_on",
                    "created_on",
                    "deleted",
                    "enabled",
                    "id",
                )
            )

            if html_tag != "":
                for template in ["create", "update"]:
                    list_update_create = Path(
                        f"{self.model_template_path}/{self.model_lower}_{template}.html"
                    )

                    if (
                        Utils.check_file_is_locked(str(list_update_create)) is True
                        and not self.force
                    ):
                        continue

                    with fileinput.FileInput(
                        list_update_create, inplace=True
                    ) as arquivo:
                        for line in arquivo:
                            print(
                                line.replace(
                                    "<!--REPLACE_PARSER_HTML-->",
                                    BeautifulSoup(html_tag, "html5lib")
                                    .prettify()
                                    .replace("<html>", "")
                                    .replace("<head>", "")
                                    .replace("</head>", "")
                                    .replace("<body>", "")
                                    .replace("</body>", "")
                                    .replace("</html>", "")
                                    .strip(),
                                ).replace(
                                    "$url_back$",
                                    f"{self.app_lower}:{self.model_lower}-list",
                                ),
                                end="",
                            )

                    with fileinput.FileInput(
                        list_update_create, inplace=True
                    ) as arquivo:
                        for line in arquivo:
                            print(
                                line.replace(
                                    "<!--REPLACE_MODAL_HTML-->", self.html_modals
                                )
                                .replace(
                                    "$url_back$",
                                    f"{self.app_lower}:{self.model_lower}-list",
                                )
                                .replace("FileLocked", "#FileLocked"),
                                end="",
                            )

                    Utils.show_message(
                        f"Template [cyan]{template}[/] parseado com sucesso"
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
            list_view = f"{self.app_lower}:{self.model_lower}-list"

            # Tenta coletar a URL,
            # caso não consiga, executa uma nova instância do manage.py com o parser
            try:
                reverse_url = reverse(list_view)

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

            fields_display = resolve(reverse_url).func.view_class.list_display
            thead = ""
            tline = ""
            for item in fields_display:
                app_field = next(
                    (
                        item_field
                        for item_field in model._meta.fields
                        if item == item_field.name
                    ),
                    None,
                )

                if app_field is not None:
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
            list_template_content = Utils.get_snippet(list_template)
            list_template_content = list_template_content.replace(
                "<!--REPLACE_THEAD-->", thead
            )
            list_template_content = list_template_content.replace(
                "<!--REPLACE_TLINE-->", tline
            )
            list_template_content = list_template_content.replace(
                "FileLocked", "#FileLocked"
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

            self.manage_create_update_templates(model)
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
