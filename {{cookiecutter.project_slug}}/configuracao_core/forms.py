from typing import Any, Dict

from django import forms

from core.forms import BaseForm
from core.utils import somente_numeros

from .models import (
    ImagensSistema,
    DadosGerais,
    Gestor,
)


class GestorForm(BaseForm):
    """Form padrão para o model Gestor"""

    telefone = forms.CharField(
        widget=forms.TextInput(
            attrs={"data-mask": "(99) 99999-9999", "placeholder": "(99) 99999-9999"}
        ),
    )

    def clean_telefone(self):
        self.cleaned_data["telefone"] = somente_numeros(self.cleaned_data["telefone"])
        if len(self.cleaned_data["telefone"]) not in {11, 10}:
            raise forms.ValidationError("Telefone inválido")
        return self.cleaned_data["telefone"]

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = Gestor


class DadosGeraisForm(BaseForm):
    """Form padrão para o model DadosGerais"""

    telefone = forms.CharField(
        widget=forms.TextInput(
            attrs={"data-mask": "(99) 99999-9999", "placeholder": "(99) 99999-9999"}
        ),
    )

    horario_atendimento = forms.CharField(
        label="Horário de atendimento",
        widget=forms.TextInput(
            attrs={
                "placeholder": "08:00 às 18:00",
            }
        ),
    )

    def clean_telefone(self):
        self.cleaned_data["telefone"] = somente_numeros(self.cleaned_data["telefone"])
        if len(self.cleaned_data["telefone"]) not in {11, 10}:
            raise forms.ValidationError("Telefone inválido")
        return self.cleaned_data["telefone"]

    def clean(self):
        if DadosGerais.objects.exists() and self.instance._state.adding:
            raise forms.ValidationError("Já existe uma configuração cadastrada")

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = DadosGerais


class ImagensSistemaForm(BaseForm):
    """Form padrão para o model ImagensSistema"""

    def clean(self) -> Dict[str, Any]:
        if ImagensSistema.objects.exists() and self.instance._state.adding:
            raise forms.ValidationError("Já existe uma configuração cadastrada")

        if len(self.cleaned_data.get("login", [])) > 3:
            raise forms.ValidationError("Só podem existir até 3 imagens de login")

        if len(self.cleaned_data.get("footer", [])) > 3:
            raise forms.ValidationError("Só podem existir até 3 imagens no rodapé")

        return self.cleaned_data

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = ImagensSistema
