import tempfile

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from PIL import Image

from configuracao_core.models import LogoSistema
from configuracao_core.views import (
    LogoSistemaCreateView,
    LogoSistemaDeleteView,
    LogoSistemaDetailView,
    LogoSistemaListView,
    LogoSistemaUpdateView,
)


class TestLogoSistemaViews:
    """Teste para as views do model LogoSistema"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste",
            email="teste@email.com.br",
            password="senha_padrao_deve_ser_mudada",
        )
        self.logosistema = baker.make(LogoSistema)

        def create_test_image():
            # Cria uma imagem aleatória com 100x100 pixels
            image = Image.new("RGB", (100, 100), color="white")
            pixels = image.load()
            for i in range(100):
                for j in range(100):
                    pixels[i, j] = (i + j, i, j)

            # Salva a imagem no diretório de mídia temporário
            with tempfile.NamedTemporaryFile(
                suffix=".jpg", dir=settings.MEDIA_ROOT
            ) as f:
                image.save(f, format="JPEG")
                f.seek(0)
                return f.read(), f.name

        # Cria uma imagem aleatória e salva-a no diretório de mídia temporário
        image_content, image_filename = create_test_image()

        # Cria o objeto de arquivo carregado com o conteúdo da imagem
        self.uploaded_file = SimpleUploadedFile(
            name="test_image.jpg", content=image_content, content_type="image/jpeg"
        )

    def test_logosistema_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:logosistema-list")
        request = self.factory.get(url)
        request.user = self.user
        response = LogoSistemaListView.as_view()(request)
        assert response.status_code == 200

    def test_logosistema_detail(self, init):
        """Teste para a view detail."""
        url = reverse(
            "configuracao_core:logosistema-detail", args={self.logosistema.pk}
        )
        request = self.factory.get(url)
        request.user = self.user
        response = LogoSistemaDetailView.as_view()(request, pk=self.logosistema.pk)
        assert response.status_code == 200

    def test_logosistema_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:logosistema-create")
        request = self.factory.get(url)
        request.user = self.user
        response = LogoSistemaCreateView.as_view()(request)
        assert response.status_code == 200

    def test_logosistema_create_post(self, init):
        """Teste para a view create usando Post."""

        data = {
            "imagem": self.uploaded_file,
        }
        url = reverse("configuracao_core:logosistema-create")
        request = self.factory.post(url)
        request.user = self.user
        response = LogoSistemaCreateView.as_view()(request, data=data, files=data)
        assert response.status_code == 200

    def test_logosistema_update(self, init):
        """Teste para a view update."""
        url = reverse(
            "configuracao_core:logosistema-update", args={self.logosistema.pk}
        )
        request = self.factory.put(url)
        request.user = self.user
        response = LogoSistemaUpdateView.as_view()(request, pk=self.logosistema.pk)
        assert response.status_code == 200

    def test_logosistema_delete(self, init):
        """Teste para a view delete."""
        url = reverse(
            "configuracao_core:logosistema-delete", args={self.logosistema.pk}
        )
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = LogoSistemaDeleteView.as_view()(request, pk=self.logosistema.pk)
        mensagem = list(messages)[0].extra_tags
        assert mensagem == "success"
        assert response.status_code == 302

    def test_logosistema_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:logosistema-list"))
        request.user = self.user
        response = LogoSistemaListView.as_view()(request)
        assert response.status_code == 200

    def test_logosistema_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:logosistema-list"))
        request.user = self.user
        response = LogoSistemaListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1
