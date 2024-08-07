from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from core.forms import ChangePasswordUserForm
from core.views.base import BaseTemplateView
from core.views.utils import get_breadcrumbs


class UpdatePassword(PasswordChangeView, BaseTemplateView):
    template_name = "core/registration/password_update.html"
    success_url = reverse_lazy("core:profile")
    model = User
    form_class = ChangePasswordUserForm

    def form_valid(self, form):
        messages.success(self.request, "Senha alterada com sucesso!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = get_breadcrumbs("core/profile/Alterar senha")
        return context
