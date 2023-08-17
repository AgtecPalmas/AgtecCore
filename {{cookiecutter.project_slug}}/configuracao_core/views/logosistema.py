from configuracao_core.forms import LogoSistemaForm
from configuracao_core.models import LogoSistema
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models LogoSistema
class LogoSistemaListView(BaseListView):
    """Classe para gerenciar a listagem do LogoSistema"""

    model = LogoSistema
    template_name = "configuracao_core/logosistema/logosistema_list.html"
    context_object_name = "logosistema"
    list_display = ["imagem", "ativo"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(LogoSistemaListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(LogoSistemaListView, self).get_queryset()
            return queryset
        else:
            queryset = super(LogoSistemaListView, self).get_queryset()
            return queryset


class LogoSistemaDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do LogoSistema"""

    model = LogoSistema
    form_class = LogoSistemaForm
    success_url = "configuracao_core:logosistema-list"
    template_name = "configuracao_core/logosistema/logosistema_detail.html"
    context_object_name = "logosistema"

    def get_context_data(self, **kwargs):
        context = super(LogoSistemaDetailView, self).get_context_data(**kwargs)
        return context


class LogoSistemaCreateView(BaseCreateView):
    """Classe para gerenciar o create do LogoSistema"""

    model = LogoSistema
    form_class = LogoSistemaForm
    context_object_name = "logosistema"
    success_url = "configuracao_core:logosistema-list"
    template_name = "configuracao_core/logosistema/logosistema_create.html"
    # inlines = []


class LogoSistemaUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do LogoSistema"""

    model = LogoSistema
    form_class = LogoSistemaForm
    context_object_name = "logosistema"
    success_url = "configuracao_core:logosistema-list"
    template_name = "configuracao_core/logosistema/logosistema_update.html"
    # inlines = []


class LogoSistemaDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do LogoSistema"""

    model = LogoSistema
    form_class = LogoSistemaForm
    context_object_name = "logosistema"
    success_url = "configuracao_core:logosistema-list"
    template_name = "configuracao_core/logosistema/logosistema_delete.html"


class LogoSistemaRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do LogoSistema"""

    model = LogoSistema
    context_object_name = "logosistema"
    success_url = "configuracao_core:logosistema-list"
    template_name = "configuracao_core/logosistema/logosistema_restore.html"


# Fim das Views do Models LogoSistema
