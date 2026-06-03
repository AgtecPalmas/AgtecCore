import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import (Gestor,)


class TestGestorModels:
    """Testes para o model Gestor"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.gestor = baker.make(Gestor)

    def test_count_gestor(self, init):
        """Testa a quantidade de gestor"""
        assert Gestor.objects.all().count() == 1

    def test_soft_delete_gestor(self, init):
        """Testa o soft delete de gestor"""
        Gestor.objects.all().delete()
        assert Gestor.objects.filter(deleted=False).count() == 0

    def test_create_gestor(self, init):
        """Testa a criação de gestor"""
        assert self.gestor.id is not None

    def test_update_gestor(self, init):
        """Testa a atualização de gestor"""
        self.gestor.save()
        self.gestor.nome = "Teste"
        self.gestor.save()
        gestor = Gestor.objects.get(nome="Teste")
        assert gestor.nome == "Teste"

    def test_str_gestor(self, init):
        """Testa a representação em string de gestor"""
        assert str(self.gestor) == f"{self.gestor.nome} - {self.gestor.funcao}"
