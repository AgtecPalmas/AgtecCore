import pytest
from faker import Faker

from configuracao_core.forms import ImagemGenericaForm


class TestImagemGenericaForms:
    """Testes para os formulários de ImagemGenerica"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()
        # TODO - Adicione campos
        self.valid_data = {}
        self.invalid_data = {}

    def test_imagemgenerica_create(self, init):
        """Teste para criação de ImagemGenerica"""
        form = ImagemGenericaForm(data=self.valid_data)
        assert form.is_valid() is True

    def teste_imagemgenerica_form_invalid(self, init):
        """Teste para formulário inválido de ImagemGenerica"""
        form = ImagemGenericaForm(data=self.invalid_data)
        assert form.is_valid() is False
