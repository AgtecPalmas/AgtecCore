from configuracao_core.forms import RedeSocialForm
from configuracao_core.models import RedeSocial
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models RedeSocial
class RedeSocialListView(BaseListView):
    """Classe para gerenciar a listagem do RedeSocial"""

    model = RedeSocial
    template_name = "configuracao_core/redesocial/redesocial_list.html"
    context_object_name = "redesocial"
    list_display = ["nome", "link", "icone"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(RedeSocialListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(RedeSocialListView, self).get_queryset()
            return queryset
        else:
            queryset = super(RedeSocialListView, self).get_queryset()
            return queryset


class RedeSocialDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do RedeSocial"""

    model = RedeSocial
    form_class = RedeSocialForm
    success_url = "configuracao_core:redesocial-list"
    template_name = "configuracao_core/redesocial/redesocial_detail.html"
    context_object_name = "redesocial"

    def get_context_data(self, **kwargs):
        context = super(RedeSocialDetailView, self).get_context_data(**kwargs)
        return context


class RedeSocialCreateView(BaseCreateView):
    """Classe para gerenciar o create do RedeSocial"""

    model = RedeSocial
    form_class = RedeSocialForm
    context_object_name = "redesocial"
    success_url = "configuracao_core:redesocial-list"
    template_name = "configuracao_core/redesocial/redesocial_create.html"
    # inlines = []


class RedeSocialUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do RedeSocial"""

    model = RedeSocial
    form_class = RedeSocialForm
    context_object_name = "redesocial"
    success_url = "configuracao_core:redesocial-list"
    template_name = "configuracao_core/redesocial/redesocial_update.html"
    # inlines = []


class RedeSocialDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do RedeSocial"""

    model = RedeSocial
    form_class = RedeSocialForm
    context_object_name = "redesocial"
    success_url = "configuracao_core:redesocial-list"
    template_name = "configuracao_core/redesocial/redesocial_delete.html"


class RedeSocialRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do RedeSocial"""

    model = RedeSocial
    context_object_name = "redesocial"
    success_url = "configuracao_core:redesocial-list"
    template_name = "configuracao_core/redesocial/redesocial_restore.html"


# Fim das Views do Models RedeSocial
