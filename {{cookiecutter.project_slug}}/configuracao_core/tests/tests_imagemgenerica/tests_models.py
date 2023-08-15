import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import ImagemGenerica


class TestImagemGenericaModels:
    """Testes para o model ImagemGenerica"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.imagemgenerica = baker.make(ImagemGenerica)

    def test_count_imagemgenerica(self, init):
        """Testa a quantidade de imagemgenerica"""
        assert ImagemGenerica.objects.all().count() == 1

    def test_soft_delete_imagemgenerica(self, init):
        """Testa o soft delete de imagemgenerica"""
        ImagemGenerica.objects.all().delete()
        assert ImagemGenerica.objects.filter(deleted=False).count() == 0

    def test_create_imagemgenerica(self, init):
        """Testa a criação de imagemgenerica"""
        assert self.imagemgenerica.id is not None

    def test_update_imagemgenerica(self, init):
        """Testa a atualização de imagemgenerica"""
        # TODO - Altere o campo e o valor
        self.imagemgenerica.save()
        self.imagemgenerica.campo = "valor"
        self.imagemgenerica.save()
        imagemgenerica = ImagemGenerica.objects.get(campo="valor")
        assert imagemgenerica.campo == "valor"
