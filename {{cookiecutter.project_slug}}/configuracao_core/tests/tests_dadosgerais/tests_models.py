import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import DadosGerais


class TestDadosGeraisModels:
    """Testes para o model DadosGerais"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.dadosgerais = baker.make(DadosGerais)

    def test_count_dadosgerais(self, init):
        """Testa a quantidade de dadosgerais"""
        assert DadosGerais.objects.all().count() == 1

    def test_soft_delete_dadosgerais(self, init):
        """Testa o soft delete de dadosgerais"""
        DadosGerais.objects.all().delete()
        assert DadosGerais.objects.filter(deleted=False).count() == 0

    def test_create_dadosgerais(self, init):
        """Testa a criação de dadosgerais"""
        assert self.dadosgerais.id is not None

    def test_update_dadosgerais(self, init):
        """Testa a atualização de dadosgerais"""
        self.dadosgerais.save()
        self.dadosgerais.telefone = "63999999999"
        self.dadosgerais.save()
        dadosgerais = DadosGerais.objects.get(telefone="63999999999")
        assert dadosgerais.telefone == "63999999999"

    def test_str_dadosgerais(self, init):
        """Testa a representação em string de dadosgerais"""
        assert self.dadosgerais.__str__() == self.dadosgerais.pk
