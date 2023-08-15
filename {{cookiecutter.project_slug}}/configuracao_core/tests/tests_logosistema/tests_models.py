import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import LogoSistema


class TestLogoSistemaModels:
    """Testes para o model LogoSistema"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.logosistema = baker.make(LogoSistema)

    def test_count_logosistema(self, init):
        """Testa a quantidade de logosistema"""
        assert LogoSistema.objects.all().count() == 1

    def test_soft_delete_logosistema(self, init):
        """Testa o soft delete de logosistema"""
        LogoSistema.objects.all().delete()
        assert LogoSistema.objects.filter(deleted=False).count() == 0

    def test_create_logosistema(self, init):
        """Testa a criação de logosistema"""
        assert self.logosistema.id is not None

    def test_update_logosistema(self, init):
        """Testa a atualização de logosistema"""
        self.logosistema.save()
        self.logosistema.ativo = False
        self.logosistema.save()
        logosistema = LogoSistema.objects.get(ativo=False)
        assert logosistema.ativo == False

    def test_str_logosistema(self, init):
        """Testa a representação em string de logosistema"""
        assert str(self.logosistema) == self.logosistema.imagem
