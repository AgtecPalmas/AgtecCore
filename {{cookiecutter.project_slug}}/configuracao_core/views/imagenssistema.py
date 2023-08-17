from configuracao_core.forms import ImagensSistemaForm
from configuracao_core.models import ImagensSistema
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models ImagensSistema
class ImagensSistemaListView(BaseListView):
    """Classe para gerenciar a listagem do ImagensSistema"""

    model = ImagensSistema
    template_name = "configuracao_core/imagenssistema/imagenssistema_list.html"
    context_object_name = "imagenssistema"
    list_display = ["login", "footer", "footer_principal", "favicon"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ImagensSistemaListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(ImagensSistemaListView, self).get_queryset()
            return queryset
        else:
            queryset = super(ImagensSistemaListView, self).get_queryset()
            return queryset


class ImagensSistemaDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do ImagensSistema"""

    model = ImagensSistema
    form_class = ImagensSistemaForm
    success_url = "configuracao_core:imagenssistema-list"
    template_name = "configuracao_core/imagenssistema/imagenssistema_detail.html"
    context_object_name = "imagenssistema"

    def get_context_data(self, **kwargs):
        context = super(ImagensSistemaDetailView, self).get_context_data(**kwargs)
        return context


class ImagensSistemaCreateView(BaseCreateView):
    """Classe para gerenciar o create do ImagensSistema"""

    model = ImagensSistema
    form_class = ImagensSistemaForm
    context_object_name = "imagenssistema"
    success_url = "configuracao_core:imagenssistema-list"
    template_name = "configuracao_core/imagenssistema/imagenssistema_create.html"
    # inlines = []


class ImagensSistemaUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do ImagensSistema"""

    model = ImagensSistema
    form_class = ImagensSistemaForm
    context_object_name = "imagenssistema"
    success_url = "configuracao_core:imagenssistema-list"
    template_name = "configuracao_core/imagenssistema/imagenssistema_update.html"
    # inlines = []


class ImagensSistemaDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do ImagensSistema"""

    model = ImagensSistema
    form_class = ImagensSistemaForm
    context_object_name = "imagenssistema"
    success_url = "configuracao_core:imagenssistema-list"
    template_name = "configuracao_core/imagenssistema/imagenssistema_delete.html"


class ImagensSistemaRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do ImagensSistema"""

    model = ImagensSistema
    context_object_name = "imagenssistema"
    success_url = "configuracao_core:imagenssistema-list"
    template_name = "configuracao_core/imagenssistema/imagenssistema_restore.html"


# Fim das Views do Models ImagensSistema
