from django.apps import AppConfig


class ConfiguracaoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "configuracao_core"
    icon = "fas fa-cogs"
    verbose_name = "Configuração"
