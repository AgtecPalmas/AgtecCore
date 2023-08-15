from configuracao_core.forms import DadosGeraisForm
from configuracao_core.models import DadosGerais
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models DadosGerais
class DadosGeraisListView(BaseListView):
    """Classe para gerenciar a listagem do DadosGerais"""

    model = DadosGerais
    template_name = "configuracao_core/dadosgerais/dadosgerais_list.html"
    context_object_name = "dadosgerais"
    list_display = ["telefone", "endereco", "horario_atendimento"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(DadosGeraisListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(DadosGeraisListView, self).get_queryset()
            return queryset
        else:
            queryset = super(DadosGeraisListView, self).get_queryset()
            return queryset


class DadosGeraisDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do DadosGerais"""

    model = DadosGerais
    form_class = DadosGeraisForm
    success_url = "configuracao_core:dadosgerais-list"
    template_name = "configuracao_core/dadosgerais/dadosgerais_detail.html"
    context_object_name = "dadosgerais"

    def get_context_data(self, **kwargs):
        context = super(DadosGeraisDetailView, self).get_context_data(**kwargs)
        return context


class DadosGeraisCreateView(BaseCreateView):
    """Classe para gerenciar o create do DadosGerais"""

    model = DadosGerais
    form_class = DadosGeraisForm
    context_object_name = "dadosgerais"
    success_url = "configuracao_core:dadosgerais-list"
    template_name = "configuracao_core/dadosgerais/dadosgerais_create.html"
    # inlines = []


class DadosGeraisUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do DadosGerais"""

    model = DadosGerais
    form_class = DadosGeraisForm
    context_object_name = "dadosgerais"
    success_url = "configuracao_core:dadosgerais-list"
    template_name = "configuracao_core/dadosgerais/dadosgerais_update.html"
    # inlines = []


class DadosGeraisDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do DadosGerais"""

    model = DadosGerais
    form_class = DadosGeraisForm
    context_object_name = "dadosgerais"
    success_url = "configuracao_core:dadosgerais-list"
    template_name = "configuracao_core/dadosgerais/dadosgerais_delete.html"


class DadosGeraisRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do DadosGerais"""

    model = DadosGerais
    context_object_name = "dadosgerais"
    success_url = "configuracao_core:dadosgerais-list"
    template_name = "configuracao_core/dadosgerais/dadosgerais_restore.html"


# Fim das Views do Models DadosGerais
