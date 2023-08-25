from core.models import Base
from django.contrib.auth.models import User
from django.db import models


class Usuario(Base):
    """Classe padrão para gerenciamento de todos os usuários da plataforma"""

    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Django User",
    )
    cpf = models.CharField("CPF", max_length=11, blank=True, null=True, unique=True)
    nome = models.CharField("Nome", max_length=300)
    email = models.EmailField("E-mail", unique=True)
    telefone = models.CharField("Telefone", max_length=100, blank=True, null=True)
    token = models.TextField("Token", blank=True, null=True, editable=False)
    firebase = models.TextField("Token Firebase", blank=True, null=True)
    access_token = models.TextField("Access Token", blank=True, null=True)
    id_token = models.TextField("ID Token", blank=True, null=True)
    latitude = models.FloatField("Latitude", default=0.0)
    longitude = models.FloatField("Longitude", default=0.0)
    endereco = models.TextField("Endereço Residencial", blank=True, null=True)

    @staticmethod
    def get_display_username(django_user):
        """
        Método responsável por retornar o atributo do usuário logado
        que será utilizado no template header_menu.html
        """
        if django_user.is_authenticated:
            if usuario := Usuario.objects.filter(django_user=django_user).first():
                return (
                    f"{usuario.nome} (Admin)"
                    if django_user.is_superuser
                    else usuario.nome
                )
            elif django_user.is_superuser:
                return f"{django_user.first_name or django_user.username} (Admin)"
            return django_user.first_name or django_user.username
        return "Visitante"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        fields_display = ["nome", "email", "telefone", "endereco"]
        icon_model = "fas fa-user"

    def __str__(self):
        return f"Usuario: {self.cpf} | {self.email}"
