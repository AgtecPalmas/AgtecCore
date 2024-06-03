from django.contrib.auth.models import User
from django.urls import reverse_lazy

from core.forms import UserUpdateForm
from core.views.base import BaseUpdateView


class ProfileUpdateView(BaseUpdateView):
    """Views para atualizar os dados do perfil do usuario"""

    model = User
    success_url = reverse_lazy("core:profile")
    form_class = UserUpdateForm
    template_name = "core/registration/profile.html"

    def get_success_message(self):
        return "Dados do perfil atualizados com sucesso"

    def get_object(self, queryset=None):
        return self.request.user

    def get_permission_required(self):
        return []

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        django_user = self.request.user
        usuario = getattr(django_user, "usuario", None)

        if usuario:
            usuario.nome = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}".strip()
            usuario.email = form.cleaned_data.get("email")
            usuario.save()

        django_user.username = email
        django_user.save()
        return super().form_valid(form)
