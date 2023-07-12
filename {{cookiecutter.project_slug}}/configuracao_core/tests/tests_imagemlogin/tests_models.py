import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import (ImagemLogin, )


class TestImagemLoginModels:
    """Testes para o model ImagemLogin"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.imagemlogin = baker.make(ImagemLogin)

    def test_count_imagemlogin(self, init):
        """Testa a quantidade de imagemlogin"""
        assert ImagemLogin.objects.all().count() == 1

    def test_soft_delete_imagemlogin(self, init):
        """Testa o soft delete de imagemlogin"""
        ImagemLogin.objects.all().delete()
        assert ImagemLogin.objects.filter(deleted=False).count() == 0

    def test_create_imagemlogin(self, init):
        """Testa a criação de imagemlogin"""
        assert self.imagemlogin.id is not None

    def test_update_imagemlogin(self, init):
        """Testa a atualização de imagemlogin"""
        self.imagemlogin.save()
        self.imagemlogin.ativo = False
        self.imagemlogin.save()
        imagemlogin = ImagemLogin.objects.get(ativo=False)
        assert imagemlogin.ativo == False

    def test_str_imagemlogin(self, init):
        """Testa a representação em string de imagemlogin"""
        assert str(self.imagemlogin) == f"{self.imagemlogin.imagem}"
