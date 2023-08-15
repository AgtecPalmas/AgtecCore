from configuracao_core.forms import GestorForm
from configuracao_core.models import Gestor
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models Gestor
class GestorListView(BaseListView):
    """Classe para gerenciar a listagem do Gestor"""

    model = Gestor
    template_name = "configuracao_core/gestor/gestor_list.html"
    context_object_name = "gestor"
    list_display = ["nome", "email", "funcao", "telefone", "assinatura"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(GestorListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(GestorListView, self).get_queryset()
            return queryset
        else:
            queryset = super(GestorListView, self).get_queryset()
            return queryset


class GestorDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Gestor"""

    model = Gestor
    form_class = GestorForm
    success_url = "configuracao_core:gestor-list"
    template_name = "configuracao_core/gestor/gestor_detail.html"
    context_object_name = "gestor"

    def get_context_data(self, **kwargs):
        context = super(GestorDetailView, self).get_context_data(**kwargs)
        return context


class GestorCreateView(BaseCreateView):
    """Classe para gerenciar o create do Gestor"""

    model = Gestor
    form_class = GestorForm
    context_object_name = "gestor"
    success_url = "configuracao_core:gestor-list"
    template_name = "configuracao_core/gestor/gestor_create.html"
    # inlines = []


class GestorUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do Gestor"""

    model = Gestor
    form_class = GestorForm
    context_object_name = "gestor"
    success_url = "configuracao_core:gestor-list"
    template_name = "configuracao_core/gestor/gestor_update.html"
    # inlines = []


class GestorDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do Gestor"""

    model = Gestor
    form_class = GestorForm
    context_object_name = "gestor"
    success_url = "configuracao_core:gestor-list"
    template_name = "configuracao_core/gestor/gestor_delete.html"


class GestorRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do Gestor"""

    model = Gestor
    context_object_name = "gestor"
    success_url = "configuracao_core:gestor-list"
    template_name = "configuracao_core/gestor/gestor_restore.html"


# Fim das Views do Models Gestor
