import pytest
from faker import Faker

from configuracao_core.forms import ImagensSistemaForm


class TestImagensSistemaForms:
    """Testes para os formulários de ImagensSistema"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()
        # TODO - Adicione campos
        self.valid_data = {}
        self.invalid_data = {}

    def test_imagenssistema_create(self, init):
        """Teste para criação de ImagensSistema"""
        form = ImagensSistemaForm(data=self.valid_data)
        assert form.is_valid() is True

    def teste_imagenssistema_form_invalid(self, init):
        """Teste para formulário inválido de ImagensSistema"""
        form = ImagensSistemaForm(data=self.invalid_data)
        assert form.is_valid() is False
