import logging
from datetime import date, datetime
from locale import normalize

import pytz
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldDoesNotExist, FieldError, ValidationError
from django.db.models import ForeignKey, Q, QuerySet
from django.db.models.fields import BooleanField as BooleanFieldModel
from django.db.models.fields import DateField, DateTimeField
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
)
from django.db.models.query_utils import DeferredAttribute
from django.views.generic import ListView

from core.models import Base
from core.views.utils import (
    get_breadcrumbs,
    get_default_context_data,
    get_url_str,
    has_fk_attr,
)

logger = logging.getLogger(__name__)


class BaseListView(
    SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView
):
    """
    Classe base que deve ser herdada caso o desenvolvedor queira reaproveitar
    as funcionalidades já desenvolvidas ListView

    Na classe que herdar dessa deve ser atribuido o valor template_name com o caminho até o template HTML a ser renderizado

    Raises:
        ValidationError -- Caso não seja atribuido o valor da variavel template_name ocorrerá uma excessão
    """

    model = Base
    list_filter = []
    search_fields = []
    list_display = list_filter + search_fields
    query_params_q = ""
    url_pagination = ""
    query_params_filters = []
    paginate_by = 1000
    template_name_suffix = "_list"

    def __init__(self):
        if self.template_name is None:
            raise ValidationError(
                message='Deve ser definido o caminho do template na variável "template_name" em sua Views!'
            )
        super(BaseListView, self).__init__()
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_permission_required(self):
        """
        cria a lista de permissões que a view pode ter de acordo com cada model.
        """
        return (
            f"{self.app_name}.view_{self.model_name}",
            f"{self.app_name}.add_{self.model_name}",
            f"{self.app_name}.delete_{self.model_name}",
            f"{self.app_name}.change_{self.model_name}",
        )

    def has_permission(self):
        """
        Verifica se tem alguma das permissões retornadas pelo
        get_permission_required, caso tenha pelo menos uma ele
        retorna True
        """
        perms = self.get_permission_required()
        # o retorno usa a função any para retornar True caso tenha pelo menos uma das permissões na lista perms
        return any(self.request.user.has_perm(perm) for perm in perms)

    def sort_queryset(
        self, queryset: QuerySet, sort_by: str, order_by: str
    ) -> QuerySet:
        """
        Ordena a queryset com base no campo e ordem especificados.

        Args:
            queryset (QuerySet): A queryset a ser ordenada.
            sort_by (str): O campo a ser ordenado.
            order_by (str): A ordem em que a queryset será ordenada. Pode ser "asc" para ascendente ou "desc" para descendente.

        Returns:
            Queryset: A queryset ordenada.

        Examples:
            >>> queryset = MyModel.objects.all()
            >>> sorted_queryset = sort_queryset(queryset, "campo", "asc")
        """

        if not hasattr(self.model, sort_by):
            messages.error(
                self.request,
                f"O campo '{sort_by}' não existe no modelo '{self.model._meta.model_name}'!",
                extra_tags="danger",
            )
            return queryset

        if order_by == "desc":
            return queryset.order_by(f"-{sort_by}")

        else:
            return queryset.order_by(sort_by)

    def get_queryset(self):
        queryset = super(BaseListView, self).get_queryset()

        if self.request.user.is_superuser:
            queryset = queryset.all()

        else:
            queryset = queryset.filter(deleted=False)

        request = self.request.GET.copy()

        sort_by = request.get("sort_by")
        order_by = request.get("order_by")

        if sort_by:
            request.pop("sort_by")
            request.pop("order_by")

            queryset = self.sort_queryset(
                queryset,
                sort_by,
                order_by,
            )

        elif (
            hasattr(self.model, "_meta")
            and hasattr(self.model._meta, "ordering")
            and self.model._meta.ordering
        ) or (
            (
                hasattr(self.model, "Meta")
                and hasattr(self.model.Meta, "ordering")
                and self.model.Meta.ordering
            )
        ):
            queryset = queryset.order_by(
                *(self.model._meta.ordering or self.model.Meta.ordering)
            )

        try:
            param_filter = request.get("q")
            query_dict = request
            query_params = Q()

            if not param_filter:
                return queryset

            for field in self.search_fields:
                try:
                    queryset.filter(**{f"{field}__icontains": param_filter})
                    query_params |= Q(**{f"{field}__icontains": param_filter})
                    continue

                except Exception as e:
                    pass

                if (
                    hasattr(self.model, field)
                    and field != ""
                    and (
                        field in ["pk", "id"] or (field.split("__")[-1] in ["pk", "id"])
                    )
                ):
                    # se for um atributo de relacionamento então olha se é numero pois pk só aceita numero.
                    if not param_filter or (param_filter and param_filter.isnumeric()):
                        query_params |= Q(**{field: param_filter})

                elif (
                    hasattr(self.model, field)
                    and type(getattr(self.model, field)) == DeferredAttribute
                ):
                    query_params |= Q(**{f"{field}__icontains": param_filter})

                elif (
                    field.split("__")[0] == "content_type"
                    and hasattr(self.model, "content_type")
                    and type(getattr(self.model, "content_type"))
                    == ForwardManyToOneDescriptor
                    and hasattr(ContentType, field.replace("content_type__", ""))
                ):
                    param_filter_content_type = param_filter
                    try:
                        param_filter_content_type = param_filter_content_type.replace(
                            " ", ""
                        ).lower()
                        param_filter_content_type = (
                            normalize("NFKD", param_filter_content_type)
                            .encode("ASCII", "ignore")
                            .decode("ASCII")
                        )

                    except Exception as erro_tipo:
                        logger.error(
                            f"Erro: {erro_tipo}; No Metodo: BaseListView.get_queryset()"
                        )
                    query_params |= Q(
                        **{f"{field}__icontains": param_filter_content_type}
                    )

                elif (
                    field.split("__")[0] == "content_object"
                    and hasattr(self.model, "content_object")
                    and type(getattr(self.model, "content_object")) == GenericForeignKey
                ):
                    try:
                        # lista de objetos genericos usados pelo model
                        list_object = queryset.values("content_type_id").distinct()
                        for obj in ContentType.objects.filter(id__in=list_object).all():
                            try:
                                # pega o campo do modelo a ser buscado
                                field_name = field.replace("content_object__", "")
                                # pega os ids dos objetos filtrados
                                list_id_object = (
                                    obj.model_class()
                                    .objects.filter(**{field_name: param_filter})
                                    .values_list("id", flat=True)
                                )

                                if len(list_id_object) > 0:
                                    query_params |= Q(
                                        content_type_id=obj.id,
                                        object_id__in=list_id_object,
                                    )

                            except Exception as erro_content:
                                logger.error(
                                    f"Erro: {erro_content}; No Metodo: BaseListView.get_queryset()"
                                )
                    except Exception as e:
                        logger.error(
                            f"Erro: {e}; No Metodo: BaseListView.get_queryset()"
                        )
                elif (
                    hasattr(self.model, field)
                    and type(getattr(self.model, field)) != ManyToManyDescriptor
                ):
                    query_params |= Q(**{field: param_filter})

            queryset = queryset.filter(query_params)

            for chave, valor in query_dict.items():
                if (
                    valor is not None
                    and valor != "None"
                    and valor != ""
                    and chave not in ["q", "csrfmiddlewaretoken", "page"]
                ):
                    not_exact = False
                    if "__not_exact" in chave:
                        not_exact = True
                        chave = f'{chave.split("__")[0]}__exact'

                    try:
                        campo_date = DateTimeField().clean(valor)
                        if not_exact:
                            queryset = queryset.exclude(**{chave: campo_date})
                        else:
                            queryset = queryset.filter(**{chave: campo_date})
                        continue

                    except Exception as e_date:
                        logger.error(
                            f"Erro: {e_date}; No Metodo: BaseListView.get_queryset()"
                        )
                    queryset = queryset.filter(**{chave: valor})

            return queryset

        except FieldError as fe:
            if field:
                # COLOQUE O extra_tags='danger' PARA CASO DE ERROS, POIS O DJANGO MANDA O NOME erro E NÃO danger QUE É PADRÃO DO BOOTSTRAP
                messages.error(
                    self.request,
                    f"Erro com o campo '{field}'!",
                    extra_tags="danger",
                )
                logger.error(f"Erro: {fe}; No Metodo: BaseListView.get_queryset()")
            return queryset.none()

        except Exception as e:
            print(e)
            messages.error(self.request, "Erro ao tentar filtrar!", extra_tags="danger")
            logger.error(f"Erro: {e}; No Metodo: BaseListView.get_queryset()")
            return queryset.none()

    def list_display_verbose_name(self):
        list_display_verbose_name = []
        for name in self.get_list_display():
            try:
                if name == "__str__":
                    if hasattr(self.model, name) and hasattr(
                        self.model._meta, "verbose_name"
                    ):
                        list_display_verbose_name.append(
                            getattr(self.model._meta, "verbose_name")
                        )

                elif (
                    "__" in name and name != "__str__" and has_fk_attr(self.model, name)
                ):
                    list_name = name.split("__")
                    list_name.reverse()
                    list_display_verbose_name.append(" ".join(list_name).title())

                elif name not in ["pk", "id"]:
                    # verifica se existe auguma função feita na view e usada no display
                    # verifica se é do tipo allow_tags
                    # e verifica se tem o short_description para usa-lo no cabeçario da tabela do list
                    if (
                        hasattr(self, name)
                        and hasattr(getattr(self, name), "allow_tags")
                        and getattr(self, name).allow_tags
                        and hasattr(getattr(self, name), "short_description")
                    ):
                        list_display_verbose_name.append(
                            getattr(self, name).short_description
                        )

                    elif hasattr(self.model, name):
                        field = self.model._meta.get_field(name)
                        if hasattr(field, "verbose_name"):
                            verbose_name = field.verbose_name.title()
                            list_display_verbose_name.append(verbose_name)
                        else:
                            list_display_verbose_name.append(name)

                    else:
                        list_display_verbose_name.append(name)

                else:
                    list_display_verbose_name.append(name)

            except FieldDoesNotExist as e:
                raise FieldDoesNotExist(
                    f"{self.model._meta.model_name} não tem nenhum campo chamado '{name}'"
                ) from e

        return list_display_verbose_name

    def list_display_plural_verbose_name(self):
        list_display_plural_verbose_name = []
        for name in self.get_list_display():
            try:
                field = self.model._meta.get_field(name)
                if name == "__str__":
                    if hasattr(self.model, name) and hasattr(
                        self.model._meta, "verbose_name_plural"
                    ):
                        list_display_plural_verbose_name.append(
                            getattr(self.model._meta, "verbose_name_plural")
                        )

                elif (
                    "__" in name and name != "__str__" and has_fk_attr(self.model, name)
                ):
                    list_name = name.split("__")
                    list_name.reverse()
                    list_display_plural_verbose_name.append(" ".join(list_name).title())

                elif name not in ["pk", "id"]:
                    # verifica se existe auguma função feita na view e usada no display
                    # verifica se é do tipo allow_tags
                    # e verifica se tem o short_description para usa-lo no cabeçario da tabela do list
                    if (
                        hasattr(self, name)
                        and hasattr(getattr(self, name), "allow_tags")
                        and getattr(self, name).allow_tags
                        and hasattr(getattr(self, name), "short_description")
                    ):
                        list_display_plural_verbose_name.append(
                            getattr(self, name).short_description
                        )

                    elif hasattr(self.model, name):
                        field = self.model._meta.get_field(name)
                        if hasattr(field, "verbose_name_plural"):
                            verbose_name = self.model._meta.get_field(
                                name
                            ).verbose_name_plural.title()
                            list_display_plural_verbose_name.append(verbose_name)
                        else:
                            list_display_plural_verbose_name.append(name)

                else:
                    list_display_plural_verbose_name.append(name)

            except FieldDoesNotExist as e:
                raise FieldDoesNotExist(
                    f"{self.model._meta.model_name} não tem nenhum campo chamado '{name}'"
                ) from e

        return list_display_plural_verbose_name

    def get_list_display(self):
        list_display = []

        # define os campos padrões
        if not self.list_display:
            self.list_display = ["pk", "__str__"]

        # define os campos padrões
        if (
            self.list_display
            and "pk" in self.list_display
            and len(self.list_display) <= 1
            and hasattr(self.model, "__str__")
        ):
            self.list_display += ["__str__"]

        # ordena para que o id sempre venha primeiro ou em segundo caso tenha o pk
        if "id" in self.list_display:
            self.list_display.remove("id")
            self.list_display = ["id"] + self.list_display

        # ordena para que o pk sempre venha primeiro
        if "pk" in self.list_display:
            self.list_display.remove("pk")

        self.list_display = ["pk"] + self.list_display

        # faz a checagem dos campos
        for name in self.list_display:
            # verifica casos onde pega campos dos filhos ex: pai__name
            if "__" in name and name != "__str__" and not has_fk_attr(self.model, name):
                messages.error(
                    self.request,
                    f"{self.model._meta.model_name} ou a View não tem nenhum campo chamado '{name}'",
                    extra_tags="danger",
                )

            elif (
                "__" not in name
                and not hasattr(self.model, name)
                and not hasattr(self, name)
            ):
                messages.error(
                    self.request,
                    f"{self.model._meta.model_name} ou a View não tem nenhum campo chamado '{name}'",
                    extra_tags="danger",
                )
                continue

            elif (
                "__" not in name
                and not hasattr(self.model, name)
                and (
                    not hasattr(getattr(self, name), "allow_tags")
                    or not getattr(self, name).allow_tags
                )
            ):
                messages.error(
                    self.request,
                    f"{self.model._meta.model_name} não tem nenhum campo chamado '{name}'",
                    extra_tags="danger",
                )
                continue

            if name not in list_display:
                list_display.append(name)

        return list_display

    def get_context_data(self, **kwargs):
        try:
            # se colocar o do super da erro de paginação
            # context = super().get_context_data(**kwargs)
            context = super(BaseListView, self).get_context_data(**kwargs)
            context = get_default_context_data(context, self)
            context["display"] = self.list_display_verbose_name()
            context["url_pagination"] = self.url_pagination

            context["model_fields"] = {
                field.name: field.verbose_name
                for field in sorted(
                    self.model._meta.fields, key=lambda field: field.name
                )
                if field.name in self.list_display
            }

            if query_params := dict(self.request.GET):
                # retira o parametro page e add ele em outra variável, apensas dele
                if query_params.get("page"):
                    query_params.pop("page")

                # retira o csrf token caso exista
                if query_params.get("csrfmiddlewaretoken"):
                    query_params.pop("csrfmiddlewaretoken")

                url_pagination = "".join(
                    f'{key}={value[0].replace(" ", "+")}&'
                    for key, value in query_params.items()
                )
                # add a url dos filtros e da pesquisa no context
                context["url_pagination"] = url_pagination

                # retira o parametro do campo de pesquisa e add ele em outra variável no context apensas dele
                if query_params.get("q"):
                    context["query_params_q"] = query_params.pop("q")[0]

                # O apps todas as verificações sobram os filtros que são add em outra variável no context apenas dele.
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
                                "id", field_display
                            )
                            for item_fk in lista_fk:
                                if item_fk["id"] == obj.id:
                                    field_dict[field_display] = (
                                        f"{item_fk[field_display]}"
                                    )

                        elif hasattr(obj, field_display) and field_display != "__str__":
                            # verifica se o campo não é None se sim entra no if
                            if obj.__getattribute__(field_display) is not None:
                                # Verificando se o campo possui o metodo do CHOICE
                                str_metodo_choice = f"get_{field_display}_display"

                                if hasattr(obj, str_metodo_choice):
                                    field_dict[field_display] = (
                                        f"{getattr(obj, str_metodo_choice)().__str__()}"
                                    )

                                elif type(getattr(obj, field_display)) == datetime:
                                    tz = pytz.timezone(settings.TIME_ZONE)
                                    campo_date_time = getattr(obj, field_display)

                                    if campo_date_time.tzinfo:
                                        date_tz = campo_date_time.astimezone(tz)

                                    else:
                                        date_tz = campo_date_time

                                    field_dict[field_display] = (
                                        f'{date_tz.strftime(settings.DATETIME_INPUT_FORMATS[0] or "%d/%m/%Y %H:%M")}'
                                    )

                                elif type(getattr(obj, field_display)) == date:
                                    field_dict[field_display] = (
                                        f'{getattr(obj, field_display).strftime(settings.DATE_INPUT_FORMATS[0] or "%d/%m/%Y")}'
                                    )

                                elif hasattr(getattr(obj, field_display), "all"):
                                    list_many = [
                                        f"{sub_obj}"
                                        for sub_obj in getattr(obj, field_display).all()
                                    ]
                                    field_dict[field_display] = ", ".join(list_many)

                                else:
                                    field_dict[field_display] = (
                                        f"{getattr(obj, field_display).__str__()}"
                                    )

                            else:
                                # no caso de campos None ele coloca para aparecer vasio
                                field_dict[field_display] = ""

                        elif field_display == "__str__":
                            field_dict[field_display] = (
                                f"{getattr(obj, field_display)()}"
                            )

                        elif (
                            hasattr(self, field_display)
                            and self.__getattribute__(field_display)
                            and field_display != "__str__"
                        ):
                            # elif verifica se existe auguma função feita na view e usada no display
                            # elif verifica se é do tipo allow_tags
                            # elif então usa o retorno da função para aparecer na lista
                            field_dict[field_display] = getattr(self, field_display)(
                                obj
                            )

                    except Exception as e:
                        logger.error(e)
                        messages.error(
                            self.request,
                            f"Erro com o campo '{field_display}' no model '{str(obj)}'!",
                            extra_tags="danger",
                        )
                        continue

                list_item.append(field_dict)

            # reinício da lista modificada para aproveitar a variavel page_list e
            # retornar apenas um objeto, no template eu separo de novo
            context["object_list"] = list_item

            object_filters = []
            # Refatorar para não precisar pecorrer os itens duas vezes
            for field in self.model._meta.fields:
                if field.name in self.list_filter:
                    # o label do choices.
                    filter_django = {}

                    # variavel para ficar no label do campo
                    label_name = " ".join(str(field.name).split("_")).title()
                    if hasattr(field, "verbose_name") and field.verbose_name:
                        label_name = field.verbose_name

                    # Verificando se o campo e relacionamento
                    if isinstance(field, ForeignKey):
                        filter_django[field.name] = {
                            "label": label_name,
                            "list": field.related_model.objects.distinct(),
                            "type_filter": "ForeignKey",
                        }

                    elif isinstance(field, BooleanFieldModel):
                        filter_django[field.name] = {
                            "label": label_name,
                            "list": ["True", "False"],
                            "type_filter": "BooleanFieldModel",
                        }

                    elif isinstance(field, (DateField, DateTimeField)):
                        # cria um choice list com os operadores que poderá usar
                        choice_date_list = [
                            {"choice_id": "__exact", "choice_label": "Igual"},
                            {
                                "choice_id": "__not_exact",
                                "choice_label": "Diferente",
                            },
                            {"choice_id": "__lt", "choice_label": "Menor que"},
                            {"choice_id": "__gt", "choice_label": "Maior que"},
                            {
                                "choice_id": "__lte",
                                "choice_label": "Menor Igual a",
                            },
                            {
                                "choice_id": "__gte",
                                "choice_label": "Maior Igual a",
                            },
                        ]
                        filter_django[field.name] = {
                            "label": label_name,
                            "list": choice_date_list,
                            "type_filter": str(type(field))[:-2].split(".")[-1],
                        }

                    elif (
                        hasattr(field, "choices")
                        and getattr(field, "choices")
                        and len(getattr(field, "choices")) > 0
                        and hasattr(field, "flatchoices")
                        and getattr(field, "flatchoices")
                        and len(getattr(field, "flatchoices")) > 0
                    ):
                        choice_list = []
                        for choice in getattr(field, "flatchoices"):
                            item = {
                                "choice_id": choice[0],
                                "choice_label": choice[1],
                            }
                            choice_list.append(item)
                        filter_django[field.name] = {
                            "label": label_name,
                            "list": choice_list,
                            "type_filter": "ChoiceField",
                        }

                    else:
                        # ele ja faz o distinct e ordena de acordo com o nome do campo
                        # add um dicionario com o nome do label, lista do filtro e o tipo de campo
                        filter_django[field.name] = {
                            "label": label_name,
                            "list": self.get_queryset()
                            .values_list(field.name, flat=True)
                            .order_by(field.attname)
                            .distinct(field.attname),
                            "type_filter": str(type(field))[:-2].split(".")[-1],
                        }

                    object_filters.append(filter_django)

            context["filters"] = object_filters

            url_str = get_url_str(context["url_list"], "Listar")
            context["breadcrumbs"] = get_breadcrumbs(url_str)
            return context

        except Exception as e:
            pass
