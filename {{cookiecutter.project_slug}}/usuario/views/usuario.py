from django.contrib.auth.views import LoginView, LogoutView

from configuracao_core.models import ImagemLogin
from core.views.base import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseListView,
    BaseRestoreView,
    BaseTemplateView,
    BaseUpdateView,
)
from core.views.utils import get_default_context_data
from usuario.forms import UsuarioForm
from usuario.models import Usuario

# Views Inicial Usuario


class UsuarioLoginView(LoginView):
    # Views para renderizar a tela inicial Usuario
    template_name = "usuario/registration/login.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method that Django calls when rendering the template.
        It allows you to add additional context variables to the template, which are then available in
        the rendered HTML. In this case, we're adding two new variables: background and logo.

        Parameters
        ----------
            self
                Represent the instance of the object
            kwargs
                Pass keyworded, variable-length argument list

        Returns
        -------

            The context of the view

        Doc Author
        ----------
            Trelent
        """
        context = super(UsuarioLoginView, self).get_context_data(**kwargs)
        context = get_default_context_data(context, self)
        context["background"] = (
            ImagemLogin.objects.filter(ativo=True, login_usuario=True)
            .order_by("?")
            .first()
        )
        return context


class UsuarioLogoutView(LogoutView):
    template_name = "usuario/registration/login.html"


class UsuarioProfileView(BaseTemplateView):
    template_name = "usuario/registration/profile.html"


# Fim das Views do Models Usuario


# Views do Models Usuario
class UsuarioListView(BaseListView):
    """Classe para gerenciar a listagem do Usuario"""

    model = Usuario
    template_name = "usuario/usuario/usuario_list.html"
    context_object_name = "usuario"
    list_display = ["nome", "email", "telefone", "endereco"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UsuarioListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        """Subscrevendo o queryset para
        filtrar os dados conforme o perfil logado

        Returns:
            QuerySet
        """

        if self.request.user.is_superuser:
            queryset = super(UsuarioListView, self).get_queryset()
            return queryset
        else:
            queryset = super(UsuarioListView, self).get_queryset()
            return queryset


class UsuarioDetailView(BaseDetailView):
    """Classe para gerenciar o detalhe do Usuario"""

    model = Usuario
    form_class = UsuarioForm
    success_url = "usuario:usuario-list"
    template_name = "usuario/usuario/usuario_detail.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super(UsuarioDetailView, self).get_context_data(**kwargs)
        return context


class UsuarioCreateView(BaseCreateView):
    """Classe para gerenciar o create do Usuario"""

    model = Usuario
    form_class = UsuarioForm
    context_object_name = "usuario"
    success_url = "usuario:usuario-list"
    template_name = "usuario/usuario/usuario_create.html"
    # inlines = []


class UsuarioUpdateView(BaseUpdateView):
    """Classe para gerenciar a update do Usuario"""

    model = Usuario
    form_class = UsuarioForm
    context_object_name = "usuario"
    success_url = "usuario:usuario-list"
    template_name = "usuario/usuario/usuario_update.html"
    # inlines = []


class UsuarioDeleteView(BaseDeleteView):
    """Classe para gerenciar o delete do Usuario"""

    model = Usuario
    form_class = UsuarioForm
    context_object_name = "usuario"
    success_url = "usuario:usuario-list"
    template_name = "usuario/usuario/usuario_delete.html"


class UsuarioRestoreView(BaseRestoreView):
    """Classe para gerenciar o restore do Usuario"""

    model = Usuario
    context_object_name = "usuario"
    success_url = "usuario:usuario-list"
    template_name = "usuario/usuario/usuario_restore.html"


# Fim das Views do Models Usuario
