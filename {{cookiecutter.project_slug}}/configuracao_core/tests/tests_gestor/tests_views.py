import pytest

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker

from configuracao_core.models import (Gestor, )
from configuracao_core.views import (GestorCreateView, GestorDeleteView,
                                           GestorDetailView, GestorListView,
                                           GestorUpdateView, )


class TestGestorViews:
    """Teste para as views do model Gestor"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username="teste", email="teste@email.com.br", password="senha_padrao_deve_ser_mudada"
        )
        self.gestor = baker.make(Gestor)

    def test_gestor_list(self, init):
        """Teste para a view list."""
        url = reverse("configuracao_core:gestor-list")
        request = self.factory.get(url)
        request.user = self.user
        response = GestorListView.as_view()(request)
        assert response.status_code == 200

    def test_gestor_detail(self, init):
        """Teste para a view detail."""
        url = reverse("configuracao_core:gestor-detail", args={self.gestor.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = GestorDetailView.as_view()(request, pk=self.gestor.pk)
        assert response.status_code == 200

    def test_gestor_create(self, init):
        """Teste para a view create."""
        url = reverse("configuracao_core:gestor-create")
        request = self.factory.get(url)
        request.user = self.user
        response = GestorCreateView.as_view()(request)
        assert response.status_code == 200

    def test_gestor_create_post(self, init):
        """Teste para a view create usando Post."""
        data = {
            "nome": self.faker.name(),
            "email": self.faker.email(),
            "funcao": self.faker.job(),
            "telefone": "69999999999",
        }
        url = reverse("configuracao_core:gestor-create")
        request = self.factory.post(url)
        request.user = self.user
        response = GestorCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_gestor_update(self, init):
        """Teste para a view update."""
        url = reverse("configuracao_core:gestor-update", args={self.gestor.pk})
        request = self.factory.put(url)
        request.user = self.user
        response = GestorUpdateView.as_view()(request, pk=self.gestor.pk)
        assert response.status_code == 200

    def test_gestor_delete(self, init):
        """Teste para a view delete."""
        url = reverse("configuracao_core:gestor-delete", args={self.gestor.pk})
        request = self.factory.delete(url)
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = GestorDeleteView.as_view()(request, pk=self.gestor.pk)
        mensagem = list(messages)[0].extra_tags
        assert mensagem == "success"
        assert response.status_code == 302

    def test_gestor_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:gestor-list"))
        request.user = self.user
        response = GestorListView.as_view()(request)
        assert response.status_code == 200

    def test_gestor_queryset_superuser(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("configuracao_core:gestor-list"))
        request.user = self.user
        response = GestorListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1
