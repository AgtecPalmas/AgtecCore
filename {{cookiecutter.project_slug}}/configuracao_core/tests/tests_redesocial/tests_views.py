import pytest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from configuracao_core.models import RedeSocial
from configuracao_core.views import (
    Configuracao_CoreIndexTemplateView,
    RedeSocialCreateView,
    RedeSocialDeleteView,
    RedeSocialDetailView,
    RedeSocialListView,
    RedeSocialUpdateView,
)


class TestRedeSocialViews:
    """Teste para as views do model RedeSocial"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste",
            email="teste@email.com.br",
            password="senha_padrao_deve_ser_mudada",
        )
        self.redesocial = baker.make(RedeSocial)

    def test_redesocial_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:redesocial-list")
        request = self.factory.get(url)
        request.user = self.user
        response = RedeSocialListView.as_view()(request)
        assert response.status_code == 200

    def test_redesocial_detail(self, init):
        """Teste para a view detail."""
        url = reverse("configuracao_core:redesocial-detail", args={self.redesocial.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = RedeSocialDetailView.as_view()(request, pk=self.redesocial.pk)
        assert response.status_code == 200

    def test_redesocial_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:redesocial-create")
        request = self.factory.get(url)
        request.user = self.user
        response = RedeSocialCreateView.as_view()(request)
        assert response.status_code == 200

    def test_redesocial_create_post(self, init):
        """Teste para a view create usando Post."""

        # TODO - Adicione campos
        data = {}
        url = reverse("configuracao_core:redesocial-create")
        request = self.factory.post(url)
        request.user = self.user
        response = RedeSocialCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_redesocial_update(self, init):
        """Teste para a view update."""
        url = reverse("configuracao_core:redesocial-update", args={self.redesocial.pk})
        request = self.factory.put(url)
        request.user = self.user
        response = RedeSocialUpdateView.as_view()(request, pk=self.redesocial.pk)
        assert response.status_code == 200

    def test_redesocial_delete(self, init):
        """Teste para a view delete."""
        url = reverse("configuracao_core:redesocial-delete", args={self.redesocial.pk})
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = RedeSocialDeleteView.as_view()(request, pk=self.redesocial.pk)
        mensagem = list(messages)[0].extra_tags
        assert mensagem == "success"
        assert response.status_code == 302

    def test_redesocial_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:redesocial-list"))
        request.user = self.user
        response = RedeSocialListView.as_view()(request)
        assert response.status_code == 200

    def test_redesocial_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:redesocial-list"))
        request.user = self.user
        response = RedeSocialListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1

    def test_configuracao_core_index(self, init):
        """Teste para a view index."""
        url = reverse("configuracao_core:configuracao_core-index")
        request = self.factory.get(url)
        request.user = self.user
        response = Configuracao_CoreIndexTemplateView.as_view()(request)
        assert response.status_code == 200
