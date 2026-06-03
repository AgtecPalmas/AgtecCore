import tempfile

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from PIL import Image

from configuracao_core.forms import (ImagemLoginForm,)
from configuracao_core.models import (ImagemLogin,)


class TestImagemLoginForms:
    """Testes para os formulários de ImagemLogin"""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker()

        def create_test_image():
            # Cria uma imagem aleatória com 100x100 pixels
            image = Image.new('RGB', (100, 100), color='white')
            pixels = image.load()
            for i in range(100):
                for j in range(100):
                    pixels[i, j] = (i + j, i, j)

            # Salva a imagem no diretório de mídia temporário
            with tempfile.NamedTemporaryFile(suffix='.jpg', dir=settings.MEDIA_ROOT) as f:
                image.save(f, format='JPEG')
                f.seek(0)
                return f.read(), f.name

        # Cria uma imagem aleatória e salva-a no diretório de mídia temporário
        image_content, image_filename = create_test_image()

        # Cria o objeto de arquivo carregado com o conteúdo da imagem
        uploaded_file = SimpleUploadedFile(name='test_image.jpg', content=image_content, content_type='image/jpeg')
        self.valid_data = {
            "imagem": uploaded_file,
            "ativo": True,
        }
        self.invalid_data = {
            "ativo": "teste",
        }

    def test_imagemlogin_create(self, init):
        """Teste para criação de ImagemLogin"""
        form = ImagemLoginForm(data=self.valid_data, files=self.valid_data)
        assert form.is_valid() is True

    def teste_imagemlogin_form_invalid(self, init):
        """Teste para formulário inválido de ImagemLogin"""
        form = ImagemLoginForm(data=self.invalid_data)
        assert form.is_valid() is False

    def test_imagemlogin_form_valid(self, init):
        """Teste para formulário válido de ImagemLogin"""
        form = ImagemLoginForm(data=self.valid_data, files=self.valid_data)
        form.save()
        assert ImagemLogin.objects.all().count() == 1
