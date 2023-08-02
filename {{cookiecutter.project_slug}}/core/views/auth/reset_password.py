from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.forms import ResetPasswordUserForm
from core.utils import get_cache, save_to_cache
from core.views.utils import get_default_context_data


class ResetPassword(FormView):
    template_name = "core/registration/password_reset.html"
    success_url = reverse_lazy("core:login")
    form_class = ResetPasswordUserForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(ResetPassword, self).get_context_data(**kwargs)
        context["title"] = "Redefinição de Senha"
        return get_default_context_data(context, self)

    def get(self, request, *args, **kwargs):
        if not get_cache(self.kwargs.get("email_code")):
            messages.error(self.request, "Código de verificação inválido")
            return redirect("core:password-request")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = get_cache(self.kwargs.get("email_code"))

        if not user_id:
            messages.error(self.request, "Código de verificação inválido")
            return redirect("core:password-request")

        save_to_cache(self.kwargs.get("email_code"), None)

        user = User.objects.get(id=user_id)

        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        messages.success(self.request, "Senha alterada com sucesso!")
        return super().form_valid(form)
