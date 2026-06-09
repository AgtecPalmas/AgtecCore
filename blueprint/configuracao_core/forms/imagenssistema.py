from typing import Any, Dict

from configuracao_core.models import ImagensSistema
from core.forms import BaseForm
from django import forms


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
        exclude = ["deleted", "enabled"]
        model = ImagensSistema
