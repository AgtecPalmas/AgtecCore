from core.forms import BaseForm

from .models import Usuario


class UsuarioForm(BaseForm):
    """Form padrão para o model Usuario"""

    class Meta:
        exclude = ["deleted", "enabled"]
        model = Usuario
