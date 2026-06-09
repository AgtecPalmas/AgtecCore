import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from usuario.models import Usuario
from usuario.views import (
    UsuarioCreateView,
    UsuarioDeleteView,
    UsuarioDetailView,
    UsuarioIndexTemplateView,
    UsuarioListView,
    UsuarioUpdateView,
)


class TestUsuarioViews:
    """Testes básicos para a views Usuario."""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.user = User.objects.create_superuser(
            username="teste", email="teste@email.com.br", password="senha_padrao_deve_ser_mudada"
        )
        baker.make(
            Usuario,
            django_user=self.user,
            cpf="12345678900",
            email="usuario@email.com.br",
        )
        baker.make(Usuario, cpf="98765432100", email="usuario2@email.com.br")
        self.factory = RequestFactory()
        self.usuario = Usuario.objects.all().first()

        """" Parametros para testar permissões de usuário"""
        self.contenttype = ContentType.objects.get_for_model(Usuario)
        self.django_usuario_dois = User.objects.create_user(
            username="usuariodois@email.com",
            email="usuariodois@email.com",
            is_staff=True,
            is_active=True,
        )
        self.usuario_permissao = Permission.objects.get(
            codename="add_usuario", content_type=self.contenttype
        )
        self.django_usuario_dois.user_permissions.add(
            self.usuario_permissao,
        )

    def test_usuario_index(self, init):
        """Testa se o template index está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-index")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioIndexTemplateView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_list(self, init):
        """Testa se o template list está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-list")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_detail(self, init):
        """Testa se o template detail está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-detail", args={self.usuario.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioDetailView.as_view()(request, pk=self.usuario.pk)
        assert response.status_code == 200

    def test_usuario_create(self, init):
        """Testa se o template create está sendo renderizado corretamente com metodo get"""
        url = reverse("usuario:usuario-create")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioCreateView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_usuario_create_post(self, init):
        """Testa se o template create está sendo renderizado corretamente com metodo post"""
        data = {
            "cpf": "12345678900",
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
        }
        url = reverse("usuario:usuario-create")
        request = self.factory.post(url)
        request.user = self.user
        response = UsuarioCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_usuario_update(self, init):
        """Testa se o template update está sendo renderizado corretamente com metodo put"""
        url = reverse("usuario:usuario-update", args={self.usuario.pk})
        request = self.factory.put(url)
        request.user = self.user
        response = UsuarioUpdateView.as_view()(request, pk=self.usuario.pk)
        assert response.status_code == 200

    def test_usuario_delete(self, init):
        """Testa a exclusão de um usuário utilizando o metodo delete"""
        usuario = self.usuario
        url = reverse("usuario:usuario-delete", args={usuario.pk})
        request = self.factory.delete(url)
        """Adiciona a sessão e a mensagem de sucesso para a requisição"""
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = UsuarioDeleteView.as_view()(request, pk=usuario.pk)
        assert response.status_code == 302

    def test_usuario_list_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_list_queryset_superuser(self, init, client):
        """Retornar a quantidade de itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 2

    """ Testes para verificar o funcionamento das permissões de usuário.
     seguindo os parametros definidos no fixture init que estão comentados"""

    @pytest.mark.skip
    def test_usuario_list_queryset_usuario_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do usuario logado"""
        client.force_login(self.django_usuario_dois)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.django_usuario_dois
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    @pytest.mark.skip
    def test_usuario_list_queryset_usuario(self, init, client):
        """Retornar a quantidade de itens cadastrados a partir do usuario logado"""
        client.force_login(self.django_usuario_dois)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.django_usuario_dois
        response = UsuarioListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1
