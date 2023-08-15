from core.views.base import BaseTemplateView


# Views Inicial Configuracao_Core
class Configuracao_CoreIndexTemplateView(BaseTemplateView):
    # Views para renderizar a tela inicial Configuracao_Core
    template_name = "configuracao_core/index.html"
    context_object_name = "configuracao_core"

    def get_context_data(self, **kwargs):
        context = super(Configuracao_CoreIndexTemplateView, self).get_context_data(
            **kwargs
        )
        return context
