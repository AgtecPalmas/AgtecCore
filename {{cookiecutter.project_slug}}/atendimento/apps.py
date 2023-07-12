from django.apps import AppConfig


class AtendimentoConfig(AppConfig):
    name = "atendimento"
    verbose_name = "Atendimento"
    icon = "fa fa-calendar"

    def ready(self):
        import atendimento.signals
