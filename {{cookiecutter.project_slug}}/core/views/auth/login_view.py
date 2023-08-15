from django.contrib.auth.views import LoginView

from core.views.utils import get_default_context_data


class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "core/registration/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return get_default_context_data(context, self)
