from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic.edit import UpdateView

from core.decorators import audit_save
from core.forms import BaseForm
from core.models import Base
from core.views.utils import get_breadcrumbs, get_default_context_data, get_url_str


class BaseRestoreView(
    SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """Classe para gerenciar a restauração dos itens do sistema
    Raises:
        ValidationError -- [Deve ser definido o caminho para o template]
    """

    model = Base
    form_class = BaseForm
    template_name_suffix = "_confirm_restore"

    def __init__(self):
        super(BaseRestoreView, self).__init__()
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_template_names(self):
        if self.template_name:
            return [
                self.template_name,
            ]
        return [
            "outside_template/base_restore.html",
        ]

    def get_success_url(self):
        try:
            self.success_message = f"'{self.object}' restaurado com sucesso"

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

            return reverse(f"{self.app_name}:{self.model_name}-list")

    def get_permission_required(self):
        """Usuário necessita da permissão delete para restaurar o item"""
        return (f"{self.app_name}.delete_{self.model_name}",)

    def get_context_data(self, **kwargs):
        context = super(BaseRestoreView, self).get_context_data(**kwargs)
        object_list, many_fields = self.object.get_all_related_fields()
        context["object_list"] = object_list
        context["many_fields"] = many_fields
        context = get_default_context_data(context, self)

        url_str = get_url_str(context["url_list"], f"Restaurar {context['object'].pk}")
        context["breadcrumbs"] = get_breadcrumbs(url_str)

        return context

    @audit_save
    def form_valid(self, form):
        form.instance.deleted = False
        form.instance.enabled = True

        # Recupera relacionamentos e os reativa também
        _, many_fields = self.object.get_all_related_fields()
        for itens in many_fields:
            obj = itens[1]
            if obj.all():
                obj.all().update(deleted=False, enabled=True)

        return super(BaseRestoreView, self).form_valid(form)
