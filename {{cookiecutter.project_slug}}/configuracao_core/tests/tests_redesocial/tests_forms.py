import pytest
from faker import Faker

from configuracao_core.forms import RedeSocialForm


class TestRedeSocialForms:
    """Testes para os formulários de RedeSocial"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()
        # TODO - Adicione campos
        self.valid_data = {}
        self.invalid_data = {}

    def test_redesocial_create(self, init):
        """Teste para criação de RedeSocial"""
        form = RedeSocialForm(data=self.valid_data)
        assert form.is_valid() is True

    def teste_redesocial_form_invalid(self, init):
        """Teste para formulário inválido de RedeSocial"""
        form = RedeSocialForm(data=self.invalid_data)
        assert form.is_valid() is False
