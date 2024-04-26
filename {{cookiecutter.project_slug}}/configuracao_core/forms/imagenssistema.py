from typing import Any, Dict

from django import forms

from configuracao_core.models import ImagemGenerica, ImagensSistema
from core.forms import BaseForm
from core.select2widgets import CoreMultipleSelect2Widget, CoreSelect2Widget


class ImagemGenericaMultipleWidget(CoreMultipleSelect2Widget):
    """Widget para o model ImagemGenerica"""

    model = ImagemGenerica
    search_fields = ["titulo__icontains"]
    attrs = {"data-minimum-input-length": 0}


class ImagemGenericaWidget(CoreSelect2Widget):
    """Widget para o model ImagemGenerica"""

    model = ImagemGenerica
    search_fields = ["titulo__icontains"]
    attrs = {"data-minimum-input-length": 0}


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
        widgets = {
            "login": ImagemGenericaMultipleWidget,
            "footer": ImagemGenericaMultipleWidget,
            "footer_principal": ImagemGenericaWidget,
        }
