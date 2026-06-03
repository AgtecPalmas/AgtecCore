import pytest
from faker import Faker
from usuario.forms import UsuarioForm
from usuario.models import Usuario


class TestUsuarioForms:
    """Testes básicos para o form Usuario."""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.valid_data = {
            "cpf": "12345678900",
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
            "password": "123456789",
            "password2": "123456789",
        }
        self.invalid_data = {
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
        }

    def test_usuario_create(self, init):
        """Teste para verificar se o form de criação de usuário é válido.
        Passando apenas os campos necessários para a criação de um usuário."""
        form = UsuarioForm(data=self.valid_data)
        assert form.is_valid() is True

    def test_usuario_form_invalid(self, init):
        """Teste para verificar se o form de criação de usuário é inválido"""
        form = UsuarioForm(data=self.invalid_data)
        assert form.is_valid() is False

    def test_usuario_form_save(self, init):
        """Teste que verifica se o form de criação de usuário salva no banco de dados"""
        form = UsuarioForm(data=self.valid_data)
        form.save()
        assert Usuario.objects.all().count() == 1
