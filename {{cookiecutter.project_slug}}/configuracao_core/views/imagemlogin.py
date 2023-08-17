from configuracao_core.forms import ImagemLoginForm
from configuracao_core.models import ImagemLogin
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseUpdateView,
)


# Views do Models ImagemLogin
class ImagemLoginListView(BaseListView):
    """Classe para gerenciar a listagem do ImagemLogin"""

    model = ImagemLogin
    template_name = "configuracao_core/imagemlogin/imagemlogin_list.html"
    context_object_name = "imagemlogin"
    list_display = ["imagem", "ativo"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ImagemLoginListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(ImagemLoginListView, self).get_queryset()
            return queryset
        else:
            queryset = super(ImagemLoginListView, self).get_queryset()
            return queryset


class ImagemLoginDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do ImagemLogin"""

    model = ImagemLogin
    form_class = ImagemLoginForm
    success_url = "configuracao_core:imagemlogin-list"
    template_name = "configuracao_core/imagemlogin/imagemlogin_detail.html"
    context_object_name = "imagemlogin"

    def get_context_data(self, **kwargs):
        context = super(ImagemLoginDetailView, self).get_context_data(**kwargs)
        return context


class ImagemLoginCreateView(BaseCreateView):
    """Classe para gerenciar o create do ImagemLogin"""

    model = ImagemLogin
    form_class = ImagemLoginForm
    context_object_name = "imagemlogin"
    success_url = "configuracao_core:imagemlogin-list"
    template_name = "configuracao_core/imagemlogin/imagemlogin_create.html"
    # inlines = []


class ImagemLoginUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do ImagemLogin"""

    model = ImagemLogin
    form_class = ImagemLoginForm
    context_object_name = "imagemlogin"
    success_url = "configuracao_core:imagemlogin-list"
    template_name = "configuracao_core/imagemlogin/imagemlogin_update.html"
    # inlines = []


class ImagemLoginDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do ImagemLogin"""

    model = ImagemLogin
    form_class = ImagemLoginForm
    context_object_name = "imagemlogin"
    success_url = "configuracao_core:imagemlogin-list"
    template_name = "configuracao_core/imagemlogin/imagemlogin_delete.html"


class ImagemLoginRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do ImagemLogin"""

    model = ImagemLogin
    context_object_name = "imagemlogin"
    success_url = "configuracao_core:imagemlogin-list"
    template_name = "configuracao_core/imagemlogin/imagemlogin_restore.html"


# Fim das Views do Models ImagemLogin
