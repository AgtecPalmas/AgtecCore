import pytest
from faker import Faker
from model_bakery import baker

from configuracao_core.models import ImagensSistema


class TestImagensSistemaModels:
    """Testes para o model ImagensSistema"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.imagenssistema = baker.make(ImagensSistema)

    def test_count_imagenssistema(self, init):
        """Testa a quantidade de imagenssistema"""
        assert ImagensSistema.objects.all().count() == 1

    def test_soft_delete_imagenssistema(self, init):
        """Testa o soft delete de imagenssistema"""
        ImagensSistema.objects.all().delete()
        assert ImagensSistema.objects.filter(deleted=False).count() == 0

    def test_create_imagenssistema(self, init):
        """Testa a criação de imagenssistema"""
        assert self.imagenssistema.id is not None

    def test_update_imagenssistema(self, init):
        """Testa a atualização de imagenssistema"""
        # TODO - Altere o campo e o valor
        self.imagenssistema.save()
        self.imagenssistema.campo = "valor"
        self.imagenssistema.save()
        imagenssistema = ImagensSistema.objects.get(campo="valor")
        assert imagenssistema.campo == "valor"
