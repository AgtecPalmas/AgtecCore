import pytest
from django.core import mail
from faker import Faker
from model_bakery import baker
from usuario.models import Usuario


class TestUsuarioModels:
    """Teste básicos para o model Usuario."""

    @pytest.fixture
    def init(self, db):
        self.faker = Faker("pt_BR")
        """Fixture para inicializar os testes utilizando baker"""
        self.usuario = baker.make(
            Usuario, cpf="15151551515", email="usuario@email.com.br"
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
            cpf="12345678900",
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
