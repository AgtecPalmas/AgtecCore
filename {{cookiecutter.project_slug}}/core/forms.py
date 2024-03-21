import secrets

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.fields import BooleanField, DateField, DateTimeField, JSONField
from django.utils.translation import gettext_lazy as _

from core.middleware.current_user import get_current_user
from usuario.models import Usuario

from .models import Audit, Base


class BaseForm(forms.ModelForm):
    """Form para ser usado no classe based views"""

    # Sobrescrevendo o Init para aplicar as regras CSS
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(BaseForm, self).__init__(*args, **kwargs)

        if "Modal" in self.__class__.__name__:
            self.update_fields_modal()

        for field in iter(self.fields):
            # Coleta as classes passadas no Form
            class_attrs: list = (
                self.fields[field].widget.attrs.get("class", "").split(" ")
            )

            # Aplica o padrão
            class_attrs.append("form-control")

            # Verificando se o campo é Booleano
            if isinstance(self.fields[field], BooleanField):
                class_attrs.append("form-check-input")

            # Verificando se o campo é do tipo DateTime
            elif isinstance(self.fields[field], DateTimeField):
                class_attrs.append("datetimefield")
                self.fields[field].widget.attrs.update(
                    {"placeholder": "dd/mm/aaaa hh:mm"}
                )
                self.fields[field].widget.input_type = "datetime-local"

            # Verificando se o campo é do tipo Date
            elif isinstance(self.fields[field], DateField):
                class_attrs.append("datefield")
                self.fields[field].widget.attrs.update({"placeholder": "dd/mm/aaaa"})
                self.fields[field].widget.input_type = "date"

            class_attrs.append(self.get_validation_class(field))

            # Atualizando os atributos do campo para adicionar as classes
            # conforme as regras anteriores
            self.fields[field].widget.attrs.update({"class": " ".join(class_attrs)})

    def update_fields_modal(self):
        """Atualiza os campos do formulário para serem usados em modais"""
        random_str = secrets.token_urlsafe(5)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {"id": f"{random_str}_{field}"}
            )

    def get_validation_class(self, field) -> str:
        """Retorna a classe de validação do campo"""
        if self.errors:
            return "is-invalid" if field in self.errors else "is-valid"
        else:
            return ""

    class Meta:
        model = Base
        exclude = ["enabled", "deleted"]


"""
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
                    Área dos models de Auditoria
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
"""


class AuditForm(forms.ModelForm):
    previous_data_change = JSONField(help_text=_("before the time of the change"))
    current_data = JSONField(help_text=_("data at the time of the change"))
    user_change = JSONField(label=_("user"), help_text=_("user who changed the data"))
    user_permissions_change = JSONField(
        label=_("user permissions"), help_text=_("permissions at the time of change")
    )
    user_groups_change = JSONField(
        label=_("user groups"), help_text=_("groups at the time of change")
    )

    class Meta:
        fields = "__all__"
        model = Audit


class ValidateUserForm(forms.Form):
    """Valida as informações do usuário para enviar o email de reset de senha"""

    model = User
    username = forms.CharField(label=_("username"), max_length=150)
    email = forms.EmailField(label=_("email"), max_length=150)

    def clean(self):
        data = self.cleaned_data
        username = data.get("username")
        email = data.get("email")

        try:
            User.objects.get(username=username, email=email)

        except User.DoesNotExist as e:
            raise forms.ValidationError("Usuário não encontrado") from e

        return data


class ResetPasswordUserForm(forms.Form):
    """Valida as informações do usuário para resetar a senha"""

    model = User
    password = forms.CharField(label=_("password"), max_length=150)
    password_confirm = forms.CharField(label=_("password_confirm"), max_length=150)

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("As senhas não conferem")

        return data


class ChangePasswordUserForm(PasswordChangeForm):
    """Valida as informações do usuário para alterar a senha"""

    old_password = forms.CharField(
        label=_("Senha Antiga"),
        max_length=150,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label=_("Nova Senha"),
        max_length=150,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label=_("Confirme a Nova Senha"),
        max_length=150,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserUpdateForm(BaseForm):

    @staticmethod
    def __valid_djangouser(user, email) -> bool:
        """Valida se o email já está cadastrado no sistema por um DjangoUser"""
        user_email = User.objects.filter(username=email)

        return user_email and user_email != user

    @staticmethod
    def __valid_usuario(user, email) -> bool:
        """Valida se o email já está cadastrado no sistema por um Usuario"""
        usuario = getattr(user, "usuario", None)
        updated_usuario = Usuario.objects.filter(email=email).first()

        if usuario and updated_usuario:
            return usuario == updated_usuario
        return not updated_usuario

    def clean_email(self):

        email = self.cleaned_data.get("email")
        django_user = get_current_user()

        if not email:
            raise forms.ValidationError("O campo email é obrigatório")

        if self.__valid_djangouser(django_user, email) is False:
            raise forms.ValidationError("Já existe um usuário com esse email")

        if self.__valid_usuario(django_user, email) is False:
            raise forms.ValidationError("Já existe um usuário com esse email")

        return email

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
