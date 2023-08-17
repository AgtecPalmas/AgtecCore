import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import RedeSocial


class TestRedeSocialModels:
    """Testes para o model RedeSocial"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.redesocial = baker.make(RedeSocial)

    def test_count_redesocial(self, init):
        """Testa a quantidade de redesocial"""
        assert RedeSocial.objects.all().count() == 1

    def test_soft_delete_redesocial(self, init):
        """Testa o soft delete de redesocial"""
        RedeSocial.objects.all().delete()
        assert RedeSocial.objects.filter(deleted=False).count() == 0

    def test_create_redesocial(self, init):
        """Testa a criação de redesocial"""
        assert self.redesocial.id is not None

    def test_update_redesocial(self, init):
        """Testa a atualização de redesocial"""
        # TODO - Altere o campo e o valor
        self.redesocial.save()
        self.redesocial.campo = "valor"
        self.redesocial.save()
        redesocial = RedeSocial.objects.get(campo="valor")
        assert redesocial.campo == "valor"
