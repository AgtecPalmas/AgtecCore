# Pytest

## Sobre

Framework para realizar testes unitários compreendendo testes de:

1 - models.py  
2 - forms.py  
3 - views.py

Na raiz do projeto existe o arquivo ```pytest.ini``` contendo a configuração necessário para que o framework identifique
os testes no projeto Django.

## Executar

```python
pytest
```

## Relatório de cobertura dos testes

    ----------- coverage: platform win32, python 3.8.6-final-0 -----------
    Name                                             Stmts   Miss  Cover
    --------------------------------------------------------------------
    __init__.py                                          0      0   100%
    usuario\__init__.py                                  1      0   100%
    usuario\admin.py                                     1      0   100%
    usuario\apps.py                                      4      0   100%
    usuario\models.py                                   43     14    67%
    usuario\tests\__init__.py                            0      0   100%
    usuario\tests\tests.py                              13      0   100%
    --------------------------------------------------------------------
    TOTAL                                               80     14    82%

    FAIL Required test coverage of 90% not reached. Total coverage: 82.50%

## Gerar a base dos testes de uma app específica

Para agilizar a criação dos testes, foi criado um comando para gerar a base dos testes de uma app específica. Este comando
irá gerar os arquivos ```tests_forms.py```, ```tests_models.py``` e ```tests_views.py``` separando-os por pastas de cada modelo
que ficará localizada dentro da pasta ```tests``` da app.

```python
python manage.py build nome_da_app --tests

```

## Exemplo de testes contidos na app usuario

Para facilitar a replicação dos testes para as apps que você desenvolver, foram criados os arquivos de
testes ```tests_forms.py```, ```tests_models.py``` e ```tests_views.py``` na app
```usuario``` contendo os testes para os models, forms e views.

### Exemplo de teste de model

```python
import pytest
from django.core import mail
from faker import Faker
from model_bakery import baker
from usuario.models import Usuario


class TestUsuarioModels:
    """Teste básicos para o model Usuario.
    Nos campos CPF geramos um valor fictício para teste 24935340002 
    no site https://www.4devs.com.br/gerador_de_cpf
    ."""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        """Fixture para inicializar os testes utilizando baker"""
        self.usuario = baker.make(
            Usuario, cpf="24935340002", email="usuario@email.com.br"
        )
        """baker cria um objeto do model Usuario com os campos obrigatórios. Se necessario passar algum campo opcional,
                 basta passar como parametro no baker.make"""

    def test_count_user(self, init):
        """Teste para verificar se o usuario se foi criado apenas um usuario"""
        assert Usuario.objects.all().count() == 1

    def test_soft_delete_user(self, init):
        """Teste para verificar se o usuario foi deletado"""
        Usuario.objects.all().delete()
        assert Usuario.objects.filter(deleted=False).count() == 0

    @pytest.mark.skip
    def test_hard_delete_user(self, init):
        assert self.usuario.delete() is True

    def test_create_user(self, init):
        """Teste para verificar se o usuario foi criado com sucesso"""
        assert self.usuario.id is not None

    def test_save_user_method(self, init):
        """Teste para verificar se o usuario foi criado com sucesso, e verificação se o count de usuarios é 2"""
        usuario = Usuario(
            cpf="24935340002",
            nome=self.faker.name(),
            email=self.faker.company_email(),
        )
        usuario.save()
        count = Usuario.objects.all().count()
        assert count == 2

    def test_update_user(self, init):
        """Teste para verificar se o usuario foi atualizado com sucesso"""
        self.usuario.nome = "Maria"
        self.usuario.save()
        usuario_email = Usuario.objects.get(nome="Maria")
        assert usuario_email.nome == "Maria"

    def test_user_str(self, init):
        """Teste para verificar a passagem de parametros para o metodo __str__"""
        assert (
            str(self.usuario) == f"Usuario: {self.usuario.cpf} | {self.usuario.email}"
        )

    def test_send_email_account_created(self, init):
        mail.send_mail(
            "Teste campo subject do email",
            "Teste campo corpo do email",
            "from@yourdjangoapp.com",
            [self.usuario.email],
            fail_silently=False,
        )
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "Teste campo subject do email"
        assert mail.outbox[0].body == "Teste campo corpo do email"
        assert mail.outbox[0].to[0] == self.usuario.email
```

### Exemplo de teste de forms

```python
import pytest
from faker import Faker
from usuario.forms import UsuarioForm
from usuario.models import Usuario


class TestUsuarioForms:
    """Testes básicos para o form Usuario."""


    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.valid_data = {
            "cpf": "24935340002",
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
            "password": "123456789",
            "password2": "123456789",
        }
        self.invalid_data = {
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
        }

    def test_usuario_create(self, init):
        """Teste para verificar se o form de criação de usuário é válido.
        Passando apenas os campos necessários para a criação de um usuário."""
        form = UsuarioForm(data=self.valid_data)
        assert form.is_valid() is True

    def test_usuario_form_invalid(self, init):
        """Teste para verificar se o form de criação de usuário é inválido"""
        form = UsuarioForm(data=self.invalid_data)
        assert form.is_valid() is False

    def test_usuario_form_save(self, init):
        """Teste que verifica se o form de criação de usuário salva no banco de dados"""
        form = UsuarioForm(data=self.valid_data)
        form.save()
        assert Usuario.objects.all().count() == 1
```

### Exemplo de teste de views

```python
import pytest
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from usuario.models import Usuario
from usuario.views import (
    UsuarioCreateView,
    UsuarioDeleteView,
    UsuarioDetailView,
    UsuarioIndexTemplateView,
    UsuarioListView,
    UsuarioUpdateView,
)

class TestUsuarioViews:
    """Testes básicos para a views Usuario."""
    
    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        self.user = User.objects.create_superuser(
            username="teste", email="teste@email.com.br", password="senha_padrao_deve_ser_mudada"
        )
        baker.make(
            Usuario,
            django_user=self.user,
            cpf="24935340002",
            email="usuario@email.com.br",
        )
        baker.make(Usuario, cpf="24935340002", email="usuario2@email.com.br")
        self.factory = RequestFactory()
        self.usuario = Usuario.objects.all().first()

        """" Parametros para testar permissões de usuário"""
        self.contenttype = ContentType.objects.get_for_model(Usuario)
        self.django_usuario_dois = User.objects.create_user(
            username="usuariodois@email.com",
            email="usuariodois@email.com",
            is_staff=True,
            is_active=True,
        )
        self.usuario_permissao = Permission.objects.get(
            codename="add_usuario", content_type=self.contenttype
        )
        self.django_usuario_dois.user_permissions.add(
            self.usuario_permissao,
        )

    def test_usuario_index(self, init):
        """Testa se o template index está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-index")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioIndexTemplateView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_list(self, init):
        """Testa se o template list está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-list")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_detail(self, init):
        """Testa se o template detail está sendo renderizado corretamente"""
        url = reverse("usuario:usuario-detail", args={self.usuario.pk})
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioDetailView.as_view()(request, pk=self.usuario.pk)
        assert response.status_code == 200

    def test_usuario_create(self, init):
        """Testa se o template create está sendo renderizado corretamente com metodo get"""
        url = reverse("usuario:usuario-create")
        request = self.factory.get(url)
        request.user = self.user
        response = UsuarioCreateView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_usuario_create_post(self, init):
        """Testa se o template create está sendo renderizado corretamente com metodo post"""
        data = {
            "cpf": "24935340002",
            "nome": self.faker.name(),
            "email": self.faker.company_email(),
        }
        url = reverse("usuario:usuario-create")
        request = self.factory.post(url)
        request.user = self.user
        response = UsuarioCreateView.as_view()(request, data=data)
        assert response.status_code == 200

    def test_usuario_update(self, init):
        """Testa se o template update está sendo renderizado corretamente com metodo put"""
        url = reverse("usuario:usuario-update", args={self.usuario.pk})
        request = self.factory.put(url)
        request.user = self.user
        response = UsuarioUpdateView.as_view()(request, pk=self.usuario.pk)
        assert response.status_code == 200

    def test_usuario_delete(self, init):
        """Testa a exclusão de um usuário utilizando o metodo delete"""
        usuario = self.usuario
        url = reverse("usuario:usuario-delete", args={usuario.pk})
        request = self.factory.delete(url)
        """Adiciona a sessão e a mensagem de sucesso para a requisição"""
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = UsuarioDeleteView.as_view()(request, pk=usuario.pk)
        assert response.status_code == 302

    def test_usuario_list_queryset_superuser_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    def test_usuario_list_queryset_superuser(self, init, client):
        """Retornar a quantidade de itens cadastrados a partir do superuser logado"""
        client.force_login(self.user)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.user
        response = UsuarioListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 2

    """ Testes para verificar o funcionamento das permissões de usuário.
     seguindo os parametros definidos no fixture init que estão comentados"""

    @pytest.mark.skip
    def test_usuario_list_queryset_usuario_status(self, init, client):
        """Retornar o status code 200 ao verificar itens cadastrados a partir do usuario logado"""
        client.force_login(self.django_usuario_dois)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.django_usuario_dois
        response = UsuarioListView.as_view()(request)
        assert response.status_code == 200

    @pytest.mark.skip
    def test_usuario_list_queryset_usuario(self, init, client):
        """Retornar a quantidade de itens cadastrados a partir do usuario logado"""
        client.force_login(self.django_usuario_dois)
        request = self.factory.get(reverse("usuario:usuario-list"))
        request.user = self.django_usuario_dois
        response = UsuarioListView.as_view()(request)
        assert len(response.context_data["object_list"]) == 1
```

## Verificar os modelos que ainda não foram testados

Para simplificar o processo de verificação, desenvolvemos um script que identifica os modelos que ainda
não foram testados. O script analisa os modelos que estão no arquivo ```models.py``` das apps do projeto e compara-os
com os testes que foram criados nos arquivos ```test_models.py```, ```test_views.py``` e ```test_forms.py``` de cada app.

```python
python manage.py check_tests 
```

## Arquivo de configuração

A linha ```addopts = --cov --cov-fail-under=90``` especifica o percentual mínimo de cobertura aceito para que o projeto
passe no processo de CI

```toml
[pytest]
DJANGO_SETTINGS_MODULE = base.settings
python_files = tests.py test_*.py *_tests.py
addopts = --cov --cov-fail-under = 90
```

## Links

| Pip                                     | Docs                                      |
-----------------------------------------|-------------------------------------------|
| [Pip](https://pypi.org/project/pytest/) | [Doc](https://docs.pytest.org/en/latest/) |
