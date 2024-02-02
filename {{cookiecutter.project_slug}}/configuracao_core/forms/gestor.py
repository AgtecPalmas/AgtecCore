from configuracao_core.models import Gestor
from core.forms import BaseForm
from core.utils import somente_numeros
from django import forms


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
        exclude = ["deleted", "enabled"]
        model = Gestor
