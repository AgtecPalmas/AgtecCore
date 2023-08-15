import pytest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from configuracao_core.models import ImagensSistema
from configuracao_core.views import (
    Configuracao_CoreIndexTemplateView,
    ImagensSistemaCreateView,
    ImagensSistemaDeleteView,
    ImagensSistemaDetailView,
    ImagensSistemaListView,
    ImagensSistemaUpdateView,
)


class TestImagensSistemaViews:
    """Teste para as views do model ImagensSistema"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste",
            email="teste@email.com.br",
            password="senha_padrao_deve_ser_mudada",
        )
        self.imagenssistema = baker.make(ImagensSistema)

    def test_imagenssistema_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:imagenssistema-list")
        request = self.factory.get(url)
        request.user = self.user
        response = ImagensSistemaListView.as_view()(request)
        assert response.status_code == 200

    def test_imagenssistema_detail(self, init):
        """Teste para a view detail."""
        url = reverse(
            "configuracao_core:imagenssistema-detail", args={self.imagenssistema.pk}
        )
        request = self.factory.get(url)
        request.user = self.user
        response = ImagensSistemaDetailView.as_view()(
            request, pk=self.imagenssistema.pk
        )
        assert response.status_code == 200

    def test_imagenssistema_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:imagenssistema-create")
        request = self.factory.get(url)
        request.user = self.user
        response = ImagensSistemaCreateView.as_view()(request)
        assert response.status_code == 200

    def test_imagenssistema_create_post(self, init):
        """Teste para a view create usando Post."""

        # TODO - Adicione campos
        data = {}
        url = reverse("configuracao_core:imagenssistema-create")
        request = self.factory.post(url)
        request.user = self.user
        response = ImagensSistemaCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_imagenssistema_update(self, init):
        """Teste para a view update."""
        url = reverse(
            "configuracao_core:imagenssistema-update", args={self.imagenssistema.pk}
        )
        request = self.factory.put(url)
        request.user = self.user
        response = ImagensSistemaUpdateView.as_view()(
            request, pk=self.imagenssistema.pk
        )
        assert response.status_code == 200

    def test_imagenssistema_delete(self, init):
        """Teste para a view delete."""
        url = reverse(
            "configuracao_core:imagenssistema-delete", args={self.imagenssistema.pk}
        )
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = ImagensSistemaDeleteView.as_view()(
            request, pk=self.imagenssistema.pk
        )
        mensagem = list(messages)[0].extra_tags
        assert mensagem == "success"
        assert response.status_code == 302

    def test_imagenssistema_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:imagenssistema-list"))
        request.user = self.user
        response = ImagensSistemaListView.as_view()(request)
        assert response.status_code == 200

    def test_imagenssistema_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:imagenssistema-list"))
        request.user = self.user
        response = ImagensSistemaListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1

    def test_configuracao_core_index(self, init):
        """Teste para a view index."""
        url = reverse("configuracao_core:configuracao_core-index")
        request = self.factory.get(url)
        request.user = self.user
        response = Configuracao_CoreIndexTemplateView.as_view()(request)
        assert response.status_code == 200
