from datetime import date, datetime

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db.models import ForeignKey
from django.db.models.fields import BooleanField as BooleanFieldModel
from django.db.models.fields import DateField, DateTimeField
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from core.models import Audit, ParameterForBase
from core.views.base import BaseListView, BaseTemplateView
from core.views.utils import (
    get_apps,
    get_breadcrumbs,
    get_default_context_data,
    has_fk_attr,
)


def data_type_display(obj):
    try:
        url_list = reverse(
            "{app}:{model}-list".format(
                app=obj.data_type.app_label, model=obj.data_type.model
            )
        )

    except Exception as e:
        url_list = None

    if url_list:
        return format_html(
            f'<a href="{url_list}" class="rounded p-1">{obj.data_type.name}</a>'
        )

    else:
        return obj.data_type.name


def objecto_pk_display(obj):
    try:
        url_list = reverse(
            "{app}:{model}-list".format(
                app=obj.data_type.app_label, model=obj.data_type.model
            )
        )

    except Exception as e:
        url_list = None

    if (
        obj.current_data
        and "pk" in obj.current_data
        and obj.current_data.get("pk", False)
    ):
        pk = obj.current_data.get("pk", "")

    elif (
        obj.previous_data_change
        and "pk" in obj.previous_data_change
        and obj.previous_data_change.get("pk", False)
    ):
        pk = obj.previous_data_change.get("pk", "")

    if url_list:
        return format_html(
            f'<a href="{url_list}{pk}/audit/" class="rounded p-1">{pk}</a>'
        )

    else:
        return pk


class AuditTemplateView(BaseTemplateView):
    # Views para renderizar a tela inicial Auditoria
    template_name = "audit/index.html"
    context_object_name = "audit"


class AuditListView(BaseListView):
    """View para gerenciar o detail do Audit"""

    model = Audit
    context_object_name = "audit"
    template_name = "audit/audit_list.html"
    list_display = [
        "created",
        "ip",
        "data_type_display",
        "objeto_pk_display",
        "tipo_revision",
        "num_revision",
    ]
    search_fields = [
        "data_type__app_label",
        "data_type__model",
        "tipo_revision",
        "ip",
        "current_data__pk",
        "previous_data_change__pk",
    ]
    list_filter = ["data_type", "created", "tipo_revision"]
    extra_context = {"parameter": ParameterForBase.objects.first}
    paginate_by = 10

    def data_type_display(self, obj):
        return data_type_display(obj)

    data_type_display.allow_tags = True
    data_type_display.short_description = "Model"

    def objeto_pk_display(self, obj):
        return objecto_pk_display(obj)

    objeto_pk_display.allow_tags = True
    objeto_pk_display.short_description = "PK do Objeto"


class AuditObjectListView(BaseListView):
    """View para gerenciar o detail do Audit"""

    model = Audit
    context_object_name = "audit"
    template_name = "audit/audit_object_list.html"
    list_display = [
        "created",
        "ip",
        "data_type_display",
        "objeto_pk_display",
        "tipo_revision",
        "num_revision",
    ]
    search_fields = [
        "data_type__app_label",
        "data_type__model",
        "tipo_revision",
        "ip",
        "current_data__pk",
        "previous_data_change__pk",
    ]
    list_filter = ["data_type", "created", "tipo_revision"]
    extra_context = {"parameter": ParameterForBase.objects.first}
    paginate_by = 10

    def data_type_display(self, obj):
        return data_type_display(obj)

    data_type_display.allow_tags = True
    data_type_display.short_description = "Model"

    def objeto_pk_display(self, obj):
        return objecto_pk_display(obj)

    objeto_pk_display.allow_tags = True
    objeto_pk_display.short_description = "PK do Objeto"

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.kwargs and "object_id" in self.kwargs and self.kwargs.get("object_id"):
            itens_kwargs = self.kwargs.get("object_id", "/").split("/")
            pk = None
            contentType = None
            if len(itens_kwargs) == 2:
                (name_app, name_model) = itens_kwargs
                contentType = ContentType.objects.filter(app_label=name_app)

            elif len(itens_kwargs) == 3:
                (name_app, name_model, pk) = itens_kwargs
                contentType = ContentType.objects.filter(
                    app_label=name_app, model=name_model
                )

            if contentType:
                queryset = queryset.filter(data_type__in=contentType.all())

            if not pk:
                return []

            if queryset.filter(previous_data_change__pk=pk).exists():
                queryset = queryset.filter(previous_data_change__pk=pk)
                return queryset

            if queryset.filter(current_data__pk=pk).exists():
                queryset = queryset.filter(current_data__pk=pk)
                return queryset

        return []

    def get_context_data(self, **kwargs):
        try:
            # nesse caso ele sobrescreve o do BaseListView, pois não é pra usar o BaseListView como super.
            context = super(BaseListView, self).get_context_data(**kwargs)
            context = get_default_context_data(context, self)
            context["display"] = self.list_display_verbose_name()

            # processa os parametros para retorna-los ao template
            query_params = dict(self.request.GET)

            if query_params:
                # retira o parametro page e add ele em outra variavel, apensas dele
                if query_params.get("page"):
                    query_params.pop("page")

                # retira o csrf token caso exista
                if query_params.get("csrfmiddlewaretoken"):
                    query_params.pop("csrfmiddlewaretoken")

                # cria a url para add ao link de paginação para não perder os filtros
                url_pagination = ""
                for key, value in query_params.items():
                    url_pagination += "{}={}&".format(key, value[0].replace(" ", "+"))

                # add a url dos filtros e da pesquisa no context
                context["url_pagination"] = url_pagination

                # retira o parametro do campo de pesquisa e add ele em outra variavel no context apensas dele
                if query_params.get("q"):
                    context["query_params_q"] = query_params.pop("q")[0]

                # O apos todas as verificações sobram os filtros que são add em outra variavel no context apenas dele.
                context["query_params_filters"] = query_params

            # manipulo a lista para tratar de forma diferente
            list_item = []
            for obj in context["object_list"]:
                field_dict = {}

                obj._meta.get_fields(include_parents=True)

                # percorre os atributos setados no list_display
                for field_display in self.get_list_display():
                    try:
                        if (
                            "__" in field_display
                            and field_display != "__str__"
                            and has_fk_attr(obj.__class__, field_display)
                        ):
                            lista_fk = context["object_list"].values(
                                "pk", field_display
                            )

                            for item_fk in lista_fk:
                                if item_fk["pk"] == obj.pk:
                                    field_dict[field_display] = "{}".format(
                                        item_fk[field_display]
                                    )

                        elif (
                            hasattr(obj, field_display)
                            and not hasattr(
                                getattr(obj, field_display), "short_description"
                            )
                            and field_display != "__str__"
                        ):
                            # verifica se o campo não é None se sim entra no if
                            if obj.__getattribute__(field_display) is not None:
                                # Verificando se o campo possui o metodo do CHOICE
                                str_metodo_choice = "get_{nome}_display".format(
                                    nome=field_display
                                )

                                if hasattr(obj, str_metodo_choice):
                                    field_dict[field_display] = "{}".format(
                                        getattr(obj, str_metodo_choice)().__str__()
                                    )

                                else:
                                    if type(getattr(obj, field_display)) == datetime:
                                        campo_date_time = getattr(obj, field_display)
                                        tz = pytz.timezone(settings.TIME_ZONE)

                                        if campo_date_time.tzinfo:
                                            date_tz = campo_date_time.astimezone(tz)

                                        else:
                                            date_tz = campo_date_time

                                        field_dict[field_display] = "{}".format(
                                            date_tz.strftime(
                                                settings.DATETIME_INPUT_FORMATS[0]
                                                or "%d/%m/%Y %H:%M"
                                            )
                                        )

                                    elif type(getattr(obj, field_display)) == date:
                                        field_dict[field_display] = "{}".format(
                                            getattr(obj, field_display).strftime(
                                                settings.DATE_INPUT_FORMATS[0]
                                                or "%d/%m/%Y"
                                            )
                                        )

                                    # verifica se é um ManyToMany
                                    elif hasattr(getattr(obj, field_display), "all"):
                                        list_many = []

                                        # pega uma string feita com o str de cada objeto da lista
                                        for sub_obj in getattr(
                                            obj, field_display
                                        ).all():
                                            list_many.append("{}".format(sub_obj))

                                        field_dict[field_display] = ", ".join(list_many)

                                    else:
                                        field_dict[field_display] = "{}".format(
                                            getattr(obj, field_display).__str__()
                                        )

                            else:
                                # no caso de campos None ele coloca para aparecer vasio
                                field_dict[field_display] = ""

                        elif field_display == "__str__":
                            field_dict[field_display] = "{}".format(
                                getattr(obj, field_display)()
                            )

                        elif (
                            hasattr(self, field_display)
                            and hasattr(
                                getattr(self, field_display), "short_description"
                            )
                            and self.__getattribute__(field_display)
                            and field_display != "__str__"
                        ):
                            # elif verifica se existe auguma função feita na view e usada no display
                            # elif verifica se é do tipo allow_tags
                            # elif então usa o retorno da função para aparecer na lista
                            if (
                                hasattr(getattr(self, field_display), "allow_tags")
                                and getattr(self, field_display).allow_tags
                            ):
                                field_dict[field_display] = mark_safe(
                                    getattr(self, field_display)(obj)
                                )

                            else:
                                field_dict[field_display] = getattr(
                                    self, field_display
                                )(obj)

                        elif (
                            hasattr(obj, field_display)
                            and hasattr(
                                getattr(obj, field_display), "short_description"
                            )
                            and obj.__getattribute__(field_display)
                            and field_display != "__str__"
                        ):
                            # elif verifica se existe auguma função feita no objeto e usada no display
                            # elif verifica se é do tipo allow_tags
                            # elif então usa o retorno da função para aparecer na lista
                            if (
                                hasattr(getattr(obj, field_display), "allow_tags")
                                and getattr(obj, field_display).allow_tags
                            ):
                                field_dict[field_display] = mark_safe(
                                    getattr(obj, field_display)()
                                )

                            else:
                                field_dict[field_display] = getattr(
                                    obj, field_display
                                )()

                    except Exception as e:
                        messages.error(
                            self.request,
                            "Erro com o campo '%s' no model '%s'!"
                            % (field_display, str(obj)),
                            extra_tags="danger",
                        )
                        continue

                list_item.append(field_dict)

            # reinciro a lista modificada para aproveitar a variavel page_list e retornar apenas um objeto, no template eu separo de novo
            context["object_list"] = list_item

            object_filters = []
            # Refatorar para não precisar pecorrer os itens duas vezes
            for field in self.model._meta.fields:
                if field.name in self.list_filter:
                    # o label do choices.
                    filter = {}

                    # variavel para ficar no label do campo
                    label_name = " ".join(str(field.name).split("_")).title()

                    if hasattr(field, "verbose_name") and field.verbose_name:
                        label_name = field.verbose_name

                    # Verificando se o campo e relacionamento
                    if isinstance(field, ForeignKey):
                        filter[field.name] = {
                            "label": label_name,
                            "list": field.related_model.objects.distinct(),
                            "type_filter": "ForeignKey",
                        }

                    # Verificando se o campo eh booleano
                    elif isinstance(field, BooleanFieldModel):
                        filter[field.name] = {
                            "label": label_name,
                            "list": ["True", "False"],
                            "type_filter": "BooleanFieldModel",
                        }

                    elif isinstance(field, DateField) or isinstance(
                        field, DateTimeField
                    ):
                        # cria um choice list com  os operadores que poderá usar
                        try:
                            choice_date_list = []
                            choice_date_list.append(
                                {"choice_id": "__exact", "choice_label": "Igual"}
                            )
                            choice_date_list.append(
                                {
                                    "choice_id": "__not_exact",
                                    "choice_label": "Diferente",
                                }
                            )
                            choice_date_list.append(
                                {"choice_id": "__lt", "choice_label": "Menor que"}
                            )
                            choice_date_list.append(
                                {"choice_id": "__gt", "choice_label": "Maior que"}
                            )
                            choice_date_list.append(
                                {"choice_id": "__lte", "choice_label": "Menor Igual a"}
                            )
                            choice_date_list.append(
                                {"choice_id": "__gte", "choice_label": "Maior Igual a"}
                            )

                            filter[field.name] = {
                                "label": label_name,
                                "list": choice_date_list,
                                "type_filter": str(type(field))[:-2].split(".")[-1],
                            }

                        except Exception:
                            pass

                    else:
                        # Verificando se o campo possui o atributo CHOICE
                        if (
                            hasattr(field, "choices")
                            and hasattr(field, "flatchoices")
                            and len(getattr(field, "flatchoices")) > 0
                        ):
                            choice_list = []

                            for choice in getattr(field, "flatchoices"):
                                item = {
                                    "choice_id": choice[0],
                                    "choice_label": choice[1],
                                }
                                choice_list.append(item)

                            filter[field.name] = {
                                "label": label_name,
                                "list": choice_list,
                                "type_filter": "ChoiceField",
                            }

                        else:
                            # ele ja faz o distinct e ordena de acordo com o nome do campo
                            # add um dicionario com o nome do label, lista do filtro e o tipo de campo
                            if self.model:
                                filter[field.name] = {
                                    "label": label_name,
                                    "list": self.model.objects.values_list(
                                        field.name, flat=True
                                    )
                                    .order_by(field.attname)
                                    .distinct(field.attname),
                                    "type_filter": str(type(field))[:-2].split(".")[-1],
                                }

                            else:
                                filter[field.name] = {
                                    "label": label_name,
                                    "list": self.get_queryset()
                                    .values_list(field.name, flat=True)
                                    .order_by(field.attname)
                                    .distinct(field.attname),
                                    "type_filter": str(type(field))[:-2].split(".")[-1],
                                }

                    object_filters.append(filter)

            context["filters"] = object_filters

            model_class = None
            id_objeto = None

            if self.kwargs and "object_id" in self.kwargs:
                itens_kwargs = self.kwargs.get("object_id", "/").split("/")

                if len(itens_kwargs) == 2:
                    (name_app, name_model) = itens_kwargs
                    contentType = ContentType.objects.filter(
                        app_label=self.model._meta.app_label, model=name_model
                    ).first()

                elif len(itens_kwargs) >= 3:
                    (name_app, name_model, pk) = itens_kwargs
                    contentType = ContentType.objects.filter(
                        app_label=name_app, model=name_model
                    ).first()

                if contentType:
                    model_class = contentType.model_class()

            if model_class:
                context["url_detail"] = "{app}:{model}-detail".format(
                    app=model_class._meta.app_label, model=model_class._meta.model_name
                )
                context["url_list"] = "{app}:{model}-list".format(
                    app=model_class._meta.app_label, model=model_class._meta.model_name
                )

                context["model_name"] = (
                    "%s - %s"
                    % (
                        model_class._meta.verbose_name_plural
                        or model_class._meta.object_name,
                        self.model._meta.verbose_name_plural
                        or self.model._meta.object_name,
                    )
                ).title()

                url_audit = reverse(context["url_list"])

                if pk:
                    context["url_audit"] = "%s%s/audit/" % (url_audit, pk)

                else:
                    context["url_audit"] = "%saudit/" % url_audit

            elif not model_class and name_app:
                context["url_detail"] = "{app}:{app}-index".format(app=name_app)
                context["url_list"] = "{app}:{app}-index".format(app=name_app)
                context["model_name"] = (
                    "%s"
                    % (
                        self.model._meta.verbose_name_plural
                        or self.model._meta.object_name
                    ).title()
                )
                context["url_audit"] = reverse(context["url_list"])

            else:
                context["url_detail"] = "{app}:{model}-detail".format(
                    app=self.model._meta.app_label, model=self.model._meta.model_name
                )
                context["url_list"] = "{app}:{model}-list".format(
                    app=self.model._meta.app_label, model=self.model._meta.model_name
                )
                context["model_name"] = (
                    "%s"
                    % (
                        self.model._meta.verbose_name_plural
                        or self.model._meta.object_name
                    ).title()
                )
                context["url_audit"] = reverse(context["url_list"])

            context["object_pk"] = pk or None
            url_str = f'{reverse(context["url_list"])}/{pk}/ Auditoria'
            context["breadcrumbs"] = get_breadcrumbs(url_str)

            context["apps"] = get_apps()

            context["has_view_permission"] = self.model().has_view_permission(
                self.request
            )
            context["has_add_permission"] = self.model().has_add_permission(
                self.request
            )
            context["has_change_permission"] = False
            context["has_delete_permission"] = False

            try:
                context["object"] = (
                    ContentType.objects.get(app_label=name_app, model=name_model)
                    .model_class()
                    .objects.get(pk=pk)
                )
            except Exception:
                pass

            return context

        except FieldDoesNotExist as fe:
            pass

        except Exception as e:
            pass
