from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic.edit import DeleteView

from core.decorators import audit_delete
from core.models import Base
from core.views.utils import get_breadcrumbs, get_default_context_data, get_url_str


class BaseDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    """Classe para gerenciar a deleção dos itens do sistema
    Raises:
        ValidationError -- [Deve ser definido o caminho para o template]
    """

    model = Base
    template_name_suffix = "_confirm_delete"

    def __init__(self):
        super(BaseDeleteView, self).__init__()
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_template_names(self):
        if self.template_name:
            return [
                self.template_name,
            ]
        return [
            "outside_template/base_delete.html",
        ]

    def get_success_url(self):
        try:
            messages.success(
                request=self.request,
                message=f"'{self.object}', Excluído com Sucesso!",
                extra_tags="success",
            )

            if self.success_url and self.success_url != "":
                return reverse(self.success_url)

            else:
                return reverse(f"{self.app_name}:{self.model_name}-list")

        except Exception:
            messages.error(
                request=self.request,
                message="Ocorreu um erro, tente novamente!",
                extra_tags="danger",
            )

            return reverse(
                f"{self.app_name}:{self.model_name}-detail",
                kwargs={"pk": self.object.pk},
            )

    def get_permission_required(self):
        """
        cria a lista de permissões que a view pode ter de acordo com cada model.
        """
        return (f"{self.app_name}.delete_{self.model_name}",)

    def get_context_data(self, **kwargs):
        context = super(BaseDeleteView, self).get_context_data(**kwargs)
        object_list, many_fields = self.object.get_all_related_fields()
        context["object_list"] = object_list
        context["many_fields"] = many_fields
        context = get_default_context_data(context, self)

        url_str = get_url_str(context["url_list"], f"Apagar {context['object'].pk}")
        context["breadcrumbs"] = get_breadcrumbs(url_str)

        return context

    @audit_delete
    def post(self, request, *args, **kwargs):
        return super(BaseDeleteView, self).delete(request, *args, **kwargs)
