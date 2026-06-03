"""Middleware para retornar o usuário corrente do sistema
"""

from threading import local
from django.utils.deprecation import MiddlewareMixin

_user = local()


class CurrentUserMiddleware(MiddlewareMixin):
    """Classe responsável pela 'captura' do usuário logado"""

    def process_request(self, request):
        _user.value = request.user


def get_current_user():
    """Métodp que deve ser chamado para retornar o usuário logado

    Returns:
        User -- Usuário logado ou None
    """
    return _user.value if hasattr(_user, "value") else None
