from core.views.base import BaseTemplateView


# Views Inicial Usuario
class UsuarioIndexTemplateView(BaseTemplateView):
    # Views para renderizar a tela inicial Usuario
    template_name = "usuario/index.html"
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        context = super(UsuarioIndexTemplateView, self).get_context_data(**kwargs)
        return context
