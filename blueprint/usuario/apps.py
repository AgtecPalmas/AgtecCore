from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    name = "usuario"
    verbose_name = "Usuário"
    icon = "fas fa-user"

    def ready(self):
        import usuario.signals
