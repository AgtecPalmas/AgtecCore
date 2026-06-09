from random import randint

from base.settings import MEDIA_URL
from django.db import models
from django.utils.html import format_html

from core.models import Base
from core.utils import get_cache, get_full_url_static, save_file_to, save_to_cache
from core.validators import FileMaxSizeValidator


class Gestor(Base):
    nome = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-mail")
    funcao = models.CharField("Função", max_length=100)
    telefone = models.CharField("Telefone", max_length=11)
    assinatura = models.ImageField(
        "Assinatura",
        upload_to=save_file_to,
        blank=True,
        null=True,
        validators=[FileMaxSizeValidator()],
    )

    def __str__(self):
        return f"{self.nome} - {self.funcao}"

    class Meta:
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"
        fields_display = ["nome", "email", "funcao", "telefone", "assinatura"]
        icon_model = "fa fa-user"
        db_table = "configuracao_gestor"


class ImagemLogin(Base):
    imagem = models.ImageField(
        "Imagem de login",
        upload_to=save_file_to,
        validators=[FileMaxSizeValidator(2)],
    )
    ativo = models.BooleanField("Ativo", default=True)
    login_usuario = models.BooleanField("Login de Usuário?", default=False)

    @staticmethod
    def get_background() -> str:
        """Retorna a imagem de login"""
        background = get_cache("background")

        if background is None:
            backgrounds = ImagemLogin.objects.filter(
                ativo=True, login_usuario=False
            ).order_by("?")

            if backgrounds:
                background = backgrounds[randint(0, len(backgrounds) - 1)].imagem.url

            else:
                background = get_full_url_static("core/images/background_login.webp")

            save_to_cache("background", background)

        return background

    def __str__(self):
        return str(self.imagem)

    class Meta:
        verbose_name = "Imagem de Login"
        verbose_name_plural = "Imagens de Login"
        fields_display = ["imagem", "ativo"]
        icon_model = "fa fa-image"
        db_table = "configuracao_imagem_login"


class LogoSistema(Base):
    imagem = models.ImageField(
        "Logo do Sistema",
        upload_to=save_file_to,
        validators=[FileMaxSizeValidator(0.5)],
    )
    ativo = models.BooleanField("Ativo", default=True)

    @staticmethod
    def get_logo() -> str:
        """Retorna a logo do sistema"""
        logo = get_cache("logo")

        if logo is None:
            logos = LogoSistema.objects.filter(ativo=True).order_by("?")

            if logos:
                logo = logos[randint(0, len(logos) - 1)].imagem.url

            else:
                logo = get_full_url_static("core/images/logo_sistema.png")

            save_to_cache("logo", logo)

        return logo

    def __str__(self):
        return str(self.imagem)

    class Meta:
        verbose_name = "Logo do Sistema"
        verbose_name_plural = "Logos do Sistema"
        fields_display = ["imagem", "ativo"]
        icon_model = "fa fa-image"
        db_table = "configuracao_logo_sistema"


class DadosGerais(Base):
    telefone = models.CharField("Telefone", max_length=11)
    endereco = models.CharField("Endereço", max_length=100)
    horario_atendimento = models.CharField("Horário de atendimento", max_length=100)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Dados Gerais"
        verbose_name_plural = "Dados Gerais"
        fields_display = ["telefone", "endereco", "horario_atendimento"]
        icon_model = "fa fa-info"
        db_table = "configuracao_dados_gerais"


class RedeSocial(Base):
    nome = models.CharField("Nome", max_length=100)
    link = models.CharField("Link", max_length=100)
    icone = models.CharField(
        "Ícone",
        max_length=100,
        help_text=format_html(
            "Ícones aqui: <a href='https://fontawesome.com/v5/search?o=r&m=free' target='_blank'>Font Awesome</a>"
        ),
    )

    @staticmethod
    def get_redes_sociais() -> list:
        """Retorna as redes sociais do sistema"""
        redes_sociais = get_cache("redes_sociais")

        if redes_sociais is None:
            redes_sociais = RedeSocial.objects.all()
            save_to_cache("redes_sociais", redes_sociais, 60 * 60 * 24)

        return redes_sociais

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Rede Social"
        verbose_name_plural = "Redes Sociais"
        fields_display = ["nome", "link", "icone"]
        icon_model = "fa fa-share-alt"
        db_table = "configuracao_rede_social"


class ImagemGenerica(Base):
    titulo = models.CharField("Título", max_length=100)
    imagem = models.ImageField(
        "Imagem",
        upload_to=save_file_to,
        validators=[FileMaxSizeValidator(1)],
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Imagem Genérica"
        verbose_name_plural = "Imagens Genéricas"
        fields_display = ["titulo", "imagem"]
        icon_model = "fa fa-image"
        db_table = "configuracao_imagem_generica"


class ImagensSistema(Base):
    login = models.ManyToManyField(
        ImagemGenerica,
        verbose_name="Imagens no Login",
        related_name="login",
    )
    footer = models.ManyToManyField(
        ImagemGenerica,
        verbose_name="Imagens no Rodapé",
        related_name="footer",
    )
    footer_principal = models.ForeignKey(
        ImagemGenerica,
        verbose_name="Imagem Principal no Rodapé",
        related_name="footer_principal",
        on_delete=models.PROTECT,
    )
    favicon = models.ImageField(
        "Favicon",
        upload_to=save_file_to,
        validators=[FileMaxSizeValidator(0.5)],
    )

    @staticmethod
    def default_images() -> dict:
        """Retorna as imagens padrão do sistema para o login e rodapé"""
        return {
            "login": [
                {"imagem": get_full_url_static("core/images/logo_1.svg")},
                {"imagem": get_full_url_static("core/images/logo_desenvolvedor.svg")},
            ],
            "footer": [
                {"imagem": get_full_url_static("core/images/logo_1.svg")},
                {"imagem": get_full_url_static("core/images/logo_2.svg")},
            ],
            "footer_principal": {
                "imagem": get_full_url_static("core/images/logo_desenvolvedor.svg")
            },
            "favicon": get_full_url_static("core/images/favicon.ico"),
        }

    @staticmethod
    def get_imagens() -> dict:
        """Retorna as imagens do sistema para o login e rodapé"""
        imagens = get_cache("imagens_sistema")

        if imagens is None:
            imagens = ImagensSistema.objects.first()

            if not imagens:
                imagens = ImagensSistema.default_images()

            else:
                imagens = {
                    "login": [
                        {"imagem": f"{MEDIA_URL}{imagem.imagem}"}
                        for imagem in imagens.login.all()
                    ],
                    "footer": [
                        {"imagem": f"{MEDIA_URL}{imagem.imagem}"}
                        for imagem in imagens.footer.all()
                    ],
                    "footer_principal": {
                        "imagem": f"{MEDIA_URL}{imagens.footer_principal.imagem}"
                    },
                    "favicon": f"{MEDIA_URL}{imagens.favicon}",
                }

                save_to_cache("imagens_sistema", imagens, 60 * 60 * 24)

        return imagens

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Imagens do Sistema"
        verbose_name_plural = "Imagens do Sistema"
        fields_display = ["login", "footer", "footer_principal", "favicon"]
        icon_model = "fa fa-image"
        db_table = "configuracao_imagens_sistema"
