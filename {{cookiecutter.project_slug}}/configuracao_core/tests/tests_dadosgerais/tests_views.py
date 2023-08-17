import pytest
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from configuracao_core.models import DadosGerais
from configuracao_core.views import (
    Configuracao_CoreIndexTemplateView,
    DadosGeraisCreateView,
    DadosGeraisDeleteView,
    DadosGeraisDetailView,
    DadosGeraisListView,
    DadosGeraisUpdateView,
)


class TestDadosGeraisViews:
    """Teste para as views do model DadosGerais"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste",
            email="teste@email.com.br",
            password="senha_padrao_deve_ser_mudada",
        )
        self.dadosgerais = baker.make(DadosGerais)

    def test_dadosgerais_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:dadosgerais-list")
        request = self.factory.get(url)
        request.user = self.user
        response = DadosGeraisListView.as_view()(request)
        assert response.status_code == 200

    def test_dadosgerais_detail(self, init):
        """Teste para a view detail."""
        url = reverse(
            "configuracao_core:dadosgerais-detail", args={self.dadosgerais.pk}
        )
        request = self.factory.get(url)
        request.user = self.user
        response = DadosGeraisDetailView.as_view()(request, pk=self.dadosgerais.pk)
        assert response.status_code == 200

    def test_dadosgerais_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:dadosgerais-create")
        request = self.factory.get(url)
        request.user = self.user
        response = DadosGeraisCreateView.as_view()(request)
        assert response.status_code == 200

    def test_dadosgerais_create_post(self, init):
        """Teste para a view create usando Post."""

        data = {
            "telefone": "69999999999",
            "endereco": self.faker.address(),
            "horario_atendimento": self.faker.time(),
        }
        url = reverse("configuracao_core:dadosgerais-create")
        request = self.factory.post(url)
        request.user = self.user
        response = DadosGeraisCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_dadosgerais_update(self, init):
        """Teste para a view update."""
        url = reverse(
            "configuracao_core:dadosgerais-update", args={self.dadosgerais.pk}
        )
        request = self.factory.put(url)
        request.user = self.user
        response = DadosGeraisUpdateView.as_view()(request, pk=self.dadosgerais.pk)
        assert response.status_code == 200

    def test_dadosgerais_delete(self, init):
        """Teste para a view delete."""
        url = reverse(
            "configuracao_core:dadosgerais-delete", args={self.dadosgerais.pk}
        )
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = DadosGeraisDeleteView.as_view()(request, pk=self.dadosgerais.pk)
        assert response.status_code == 302

    def test_dadosgerais_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:dadosgerais-list"))
        request.user = self.user
        response = DadosGeraisListView.as_view()(request)
        assert response.status_code == 200

    def test_dadosgerais_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:dadosgerais-list"))
        request.user = self.user
        response = DadosGeraisListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1

    def test_configuracao_core_index(self, init):
        """Teste para a view index."""
        url = reverse("configuracao_core:configuracao_core-index")
        request = self.factory.get(url)
        request.user = self.user
        response = Configuracao_CoreIndexTemplateView.as_view()(request)
        assert response.status_code == 200
