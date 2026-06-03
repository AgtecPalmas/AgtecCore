import pytest

from faker import Faker

from configuracao_core.forms import (GestorForm, )
from configuracao_core.models import (Gestor, )


class TestGestorForms:
    """Testes para os formulários de Gestor"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()
        self.valid_data = {
            'nome': self.faker.name(),
            'email': self.faker.email(),
            'funcao': self.faker.job(),
            'telefone': "63999999999",

        }
        self.invalid_data = {
            'nome': self.faker.name(),
            'email': self.faker.email(),
            'funcao': self.faker.job(),
        }

    def test_gestor_create(self, init):
        """Teste para criação de Gestor"""
        form = GestorForm(data=self.valid_data)
        assert form.is_valid() is True

    def teste_gestor_form_invalid(self, init):
        """Teste para formulário inválido de Gestor"""
        form = GestorForm(data=self.invalid_data)
        assert form.is_valid() is False

    def test_gestor_form_save(self, init):
        """Teste para verificar se o form de criação de Gestor salva no banco de dados"""
        form = GestorForm(data=self.valid_data)
        form.save()
        assert Gestor.objects.all().count() == 1
