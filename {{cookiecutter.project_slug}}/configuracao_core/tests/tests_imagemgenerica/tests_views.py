import pytest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from configuracao_core.models import ImagemGenerica
from configuracao_core.views import (
    Configuracao_CoreIndexTemplateView,
    ImagemGenericaCreateView,
    ImagemGenericaDeleteView,
    ImagemGenericaDetailView,
    ImagemGenericaListView,
    ImagemGenericaUpdateView,
)


class TestImagemGenericaViews:
    """Teste para as views do model ImagemGenerica"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste",
            email="teste@email.com.br",
            password="senha_padrao_deve_ser_mudada",
        )
        self.imagemgenerica = baker.make(ImagemGenerica)

    def test_imagemgenerica_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:imagemgenerica-list")
        request = self.factory.get(url)
        request.user = self.user
        response = ImagemGenericaListView.as_view()(request)
        assert response.status_code == 200

    def test_imagemgenerica_detail(self, init):
        """Teste para a view detail."""
        url = reverse(
            "configuracao_core:imagemgenerica-detail", args={self.imagemgenerica.pk}
        )
        request = self.factory.get(url)
        request.user = self.user
        response = ImagemGenericaDetailView.as_view()(
            request, pk=self.imagemgenerica.pk
        )
        assert response.status_code == 200

    def test_imagemgenerica_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:imagemgenerica-create")
        request = self.factory.get(url)
        request.user = self.user
        response = ImagemGenericaCreateView.as_view()(request)
        assert response.status_code == 200

    def test_imagemgenerica_create_post(self, init):
        """Teste para a view create usando Post."""

        # TODO - Adicione campos
        data = {}
        url = reverse("configuracao_core:imagemgenerica-create")
        request = self.factory.post(url)
        request.user = self.user
        response = ImagemGenericaCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_imagemgenerica_update(self, init):
        """Teste para a view update."""
        url = reverse(
            "configuracao_core:imagemgenerica-update", args={self.imagemgenerica.pk}
        )
        request = self.factory.put(url)
        request.user = self.user
        response = ImagemGenericaUpdateView.as_view()(
            request, pk=self.imagemgenerica.pk
        )
        assert response.status_code == 200

    def test_imagemgenerica_delete(self, init):
        """Teste para a view delete."""
        url = reverse(
            "configuracao_core:imagemgenerica-delete", args={self.imagemgenerica.pk}
        )
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = ImagemGenericaDeleteView.as_view()(
            request, pk=self.imagemgenerica.pk
        )
        mensagem = list(messages)[0].extra_tags
        assert mensagem == "success"
        assert response.status_code == 302

    def test_imagemgenerica_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:imagemgenerica-list"))
        request.user = self.user
        response = ImagemGenericaListView.as_view()(request)
        assert response.status_code == 200

    def test_imagemgenerica_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:imagemgenerica-list"))
        request.user = self.user
        response = ImagemGenericaListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1

    def test_configuracao_core_index(self, init):
        """Teste para a view index."""
        url = reverse("configuracao_core:configuracao_core-index")
        request = self.factory.get(url)
        request.user = self.user
        response = Configuracao_CoreIndexTemplateView.as_view()(request)
        assert response.status_code == 200
