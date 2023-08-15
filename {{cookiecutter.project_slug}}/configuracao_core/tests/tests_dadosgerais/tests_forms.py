import pytest
from faker import Faker

from configuracao_core.forms import DadosGeraisForm
from configuracao_core.models import DadosGerais


class TestDadosGeraisForms:
    """Testes para os formulários de DadosGerais"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()
        self.valid_data = {
            "telefone": "69999999999",
            "endereco": self.faker.address(),
            "horario_atendimento": self.faker.time(),
        }
        self.invalid_data = {
            "endereco": self.faker.address(),
            "horario_atendimento": self.faker.time(),
        }

    def test_dadosgerais_create(self, init):
        """Teste para criação de DadosGerais"""
        form = DadosGeraisForm(data=self.valid_data)
        assert form.is_valid() is True

    def teste_dadosgerais_form_invalid(self, init):
        """Teste para formulário inválido de DadosGerais"""
        form = DadosGeraisForm(data=self.invalid_data)
        assert form.is_valid() is False

    def test_dadosgerais_form_save(self, init):
        """Teste para verificar se o form de criação de DadosGerais salva no banco de dados"""
        form = DadosGeraisForm(data=self.valid_data)
        form.save()
        assert DadosGerais.objects.all().count() == 1
