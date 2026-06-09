from django.utils.deprecation import MiddlewareMixin

from base.settings import BREAD_CRUMBS, HEADER_ACTIONS, HEADER_COMPLETO, HEADER_VERTICAL


class HeaderControlMiddleware(MiddlewareMixin):
    """
    Middleware para controlar se deve ter o header e o menu vertical
    utilizando as variáveis HEADER_COMPLETO, HEADER_ACTIONS e HEADER_VERTICAL
    do arquivo settings.py
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.header_completo = HEADER_COMPLETO
        request.header_actions = HEADER_ACTIONS
        request.header_vertical = HEADER_VERTICAL
        request.bread_crumbs = BREAD_CRUMBS
        return self.get_response(request)
