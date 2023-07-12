from django.contrib.auth.views import LoginView

from base.settings import SYSTEM_NAME
from configuracao_core.models import ImagensSistema, ImagemLogin, LogoSistema


class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "core/registration/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["background"] = ImagemLogin.get_background()
        context["logo_sistema"] = LogoSistema.get_logo()
        context["system_name"] = SYSTEM_NAME
        context["imagens_sistema"] = ImagensSistema.get_imagens()
        return context
