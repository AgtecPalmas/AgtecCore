import pytest
from django.contrib.auth.models import User
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from validate_docbr import CPF

from usuario.models import Usuario


class TestUsuarioAPI:
    # Definindo o endpoint da API de usuários
    @pytest.fixture
    def init(self, db):
        # Instanciando o Faker para quando for necessário gerar dados de teste no padrão PT-BR
        self.faker = Faker("pt_BR")
        # Criando um usuário para ser usado como autenticação
        django_user = User.objects.create_superuser(
            username="teste", password="Teste@1234"
        )
        # Criando um registro mocado no banco de dados de test.
        self.usuario = Usuario.objects.create(
            django_user=django_user,
            nome=self.faker.name(),
            email=self.faker.email(),
            longitude=self.faker.longitude(),
            latitude=self.faker.latitude(),
        )
        # Criando um token para o usuário
        self.token = Token.objects.get_or_create(user=django_user)[0]
        # Instanciando um cliente para fazer requisições
        self.client = APIClient()
        # Definindo as credenciais de autenticação do usuário
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        # Definindo o endpoint da API de usuários
        self.endpoint = "/usuario/api/v1/usuario/"

    def test_delete_user(self, init):
        usuario = Usuario.objects.filter().first()
        endpoint = f"{self.endpoint}{usuario.pk}/"
        request = self.client.delete(endpoint)
        assert request.status_code == 204

    def test_list_count_users(self, init):
        request = self.client.get(self.endpoint)
        assert len(request.json()["results"]) == 10

    def test_list(self, init):
        request = self.client.get(self.endpoint)
        assert request.status_code == 200

    def test_get_one_user(self, init):
        usuario = Usuario.objects.filter().first()
        request = self.client.get(f"{self.endpoint}{usuario.id}/")
        assert request.status_code == 200

    def test_create_user(self, init):
        cpf = CPF().generate()
        nome = self.faker.name()
        email = f"{nome.lower()}@{self.faker.free_email_domain()}".replace(" ", "")
        telefone = self.faker.phone_number()
        endereco_comercial = self.faker.address()
        data = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "endereco": endereco_comercial,
        }
        request = self.client.post(self.endpoint, data, format="json")
        assert request.status_code == 201

    def test_update_user(self, init):
        usuario = Usuario.objects.filter().order_by("?").first()
        nome = self.faker.name()
        email = f"{nome.lower()}@{self.faker.free_email_domain()}".replace(" ", "")
        telefone = self.faker.phone_number()
        endereco_comercial = self.faker.address()
        data = {
            "id": usuario.pk,
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": endereco_comercial,
        }
        endpoint = f"{self.endpoint}{usuario.pk}/"
        request = self.client.put(endpoint, data, format="json")
        assert request.status_code == 200
