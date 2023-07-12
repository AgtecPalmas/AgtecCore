from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import DetailView

from core.models import Base
from core.views.utils import get_breadcrumbs, get_default_context_data


class BaseDetailView(
    SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    """
    Classe base que deve ser herdada caso o desenvolvedor queira reaproveitar
    as funcionalidades já desenvolvidas para DetailView
    Na classe que herdar dessa deve ser atribuido o valor template_name com o caminho até o template HTML a ser renderizado

    Raises:
        ValidationError -- Caso não seja atribuido o valor da variavel template_name ocorrerá uma excessão
    """

    model = Base
    exclude = []
    template_name_suffix = "_detail"

    def __init__(self):
        super(BaseDetailView, self).__init__()
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_template_names(self):
        if self.template_name:
            return [
                self.template_name,
            ]

        return [
            "outside_template/base_detail.html",
        ]

    def get_permission_required(self):
        """
        cria a lista de permissões que a view pode ter de acordo com cada model.
        """

        return (
            f"{self.app_name}.view_{self.model_name}",
            f"{self.app_name}.change_{self.model_name}",
            f"{self.app_name}.delete_{self.model_name}",
            f"{self.app_name}.add_{self.model_name}",
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

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)
        object_list, many_fields = self.object.get_all_related_fields()
        context["object_list"] = object_list
        context["many_fields"] = many_fields
        context = get_default_context_data(context, self)

        url_str = reverse(context["url_list"]) + f' Detalhe {context["object"].pk}'

        context["breadcrumbs"] = get_breadcrumbs(url_str)
        return context
