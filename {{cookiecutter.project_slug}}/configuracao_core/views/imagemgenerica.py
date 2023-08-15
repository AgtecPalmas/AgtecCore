from configuracao_core.forms import ImagemGenericaForm
from configuracao_core.models import ImagemGenerica
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models ImagemGenerica
class ImagemGenericaListView(BaseListView):
    """Classe para gerenciar a listagem do ImagemGenerica"""

    model = ImagemGenerica
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_list.html"
    context_object_name = "imagemgenerica"
    list_display = ["titulo", "imagem"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ImagemGenericaListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(ImagemGenericaListView, self).get_queryset()
            return queryset
        else:
            queryset = super(ImagemGenericaListView, self).get_queryset()
            return queryset


class ImagemGenericaDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do ImagemGenerica"""

    model = ImagemGenerica
    form_class = ImagemGenericaForm
    success_url = "configuracao_core:imagemgenerica-list"
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_detail.html"
    context_object_name = "imagemgenerica"

    def get_context_data(self, **kwargs):
        context = super(ImagemGenericaDetailView, self).get_context_data(**kwargs)
        return context


class ImagemGenericaCreateView(BaseCreateView):
    """Classe para gerenciar o create do ImagemGenerica"""

    model = ImagemGenerica
    form_class = ImagemGenericaForm
    context_object_name = "imagemgenerica"
    success_url = "configuracao_core:imagemgenerica-list"
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_create.html"
    # inlines = []


class ImagemGenericaUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do ImagemGenerica"""

    model = ImagemGenerica
    form_class = ImagemGenericaForm
    context_object_name = "imagemgenerica"
    success_url = "configuracao_core:imagemgenerica-list"
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_update.html"
    # inlines = []


class ImagemGenericaDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do ImagemGenerica"""

    model = ImagemGenerica
    form_class = ImagemGenericaForm
    context_object_name = "imagemgenerica"
    success_url = "configuracao_core:imagemgenerica-list"
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_delete.html"


class ImagemGenericaRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do ImagemGenerica"""

    model = ImagemGenerica
    context_object_name = "imagemgenerica"
    success_url = "configuracao_core:imagemgenerica-list"
    template_name = "configuracao_core/imagemgenerica/imagemgenerica_restore.html"


# Fim das Views do Models ImagemGenerica
