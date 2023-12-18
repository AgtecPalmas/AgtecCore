from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class ProfileUpdateView(LoginRequiredMixin, View):
    """Views para atualizar os dados do perfil do usuario"""

    def get(self, request, *args, **kwargs):
        return redirect("core:profile")

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            request.user.first_name = data.get("first_name")
            request.user.last_name = data.get("last_name")
            request.user.email = data.get("email")
            request.user.save()
            messages.success(request, "Dados do perfil atualizados com sucesso")

        except Exception:
            messages.error(request, "Erro ao atualizar os dados do perfil")

        return redirect("core:profile")  # Redirect using name url parameter
