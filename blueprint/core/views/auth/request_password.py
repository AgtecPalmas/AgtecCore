import secrets
import string

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from sentry_sdk import capture_exception

from base.settings import DEFAULT_FROM_EMAIL, PROJECT_NAME
from core.forms import ValidateUserForm
from core.utils import get_cache, save_to_cache
from core.views.utils import get_default_context_data


class RequestPassword(FormView):
    template_name = "core/registration/password_request.html"
    success_url = reverse_lazy("core:login")
    form_class = ValidateUserForm
    model = User

    @staticmethod
    def __generate_email_link() -> str:
        """Gera um link de redefinição de senha"""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(128))

    @staticmethod
    def __send_email(email_link: str, emails: list) -> bool:
        """Envia o e-mail de redefinição de senha"""

        try:
            send_mail(
                subject=f"Redefinição de Senha - {PROJECT_NAME}",
                message="",
                html_message=f"""Recemos uma solicitação de redefinição de senha para sua conta
            <br/>Se você não fez essa solicitação, ignore este e-mail
            <br/>Acesse o link abaixo para redefinir sua senha
            <br/><br/><a href="{email_link}" target="_blank">{email_link}</a>
            <br/>O link é válido por 5 minutos""",
                recipient_list=emails,
                from_email=DEFAULT_FROM_EMAIL,
            )
            return True

        except Exception as e:
            capture_exception(e)
            return False

    @staticmethod
    def __get_email_code(user: User) -> tuple:
        """Retorna o link de redefinição de senha do usuário e a quantidade de tentativas"""
        email_code: str = None
        attemps: int = 1

        cache = get_cache(str(user.id))

        if cache:
            email_code, attemps = (
                cache.get("email_code"),
                cache.get("attempts"),
            )

        # Usa o mesmo link
        if email_code:
            save_to_cache(
                str(user.id),
                {
                    "email_code": email_code,
                    "attempts": int(attemps) + 1,
                },
            )
            return (email_code, attemps)

        # Gera um novo link
        email_code = RequestPassword.__generate_email_link()
        save_to_cache(email_code, user.id)
        save_to_cache(
            str(user.id),
            {
                "email_code": email_code,
                "attempts": attemps,
            },
        )

        return (email_code, attemps)

    def get_context_data(self, **kwargs):
        context = super(RequestPassword, self).get_context_data(**kwargs)
        context["title"] = "Redefinição de Senha"
        return get_default_context_data(context, self)

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data["username"])

        email_code, attempts = self.__get_email_code(user)

        if attempts >= 3:
            messages.error(
                self.request,
                "Você excedeu o número de tentativas, tente novamente mais tarde",
            )
            return super().form_invalid(form)

        email_link = self.request.build_absolute_uri(
            reverse_lazy("core:password-reset", kwargs={"email_code": email_code})
        )

        if not self.__send_email(email_link, [user.email]):
            messages.error(
                self.request,
                "Erro ao enviar e-mail de redefinição de senha, tente novamente",
            )
            return super().form_invalid(form)

        messages.success(
            self.request,
            f"E-mail com link para redefinição de senha enviado com sucesso para {user.email}",
        )
        return super().form_valid(form)
