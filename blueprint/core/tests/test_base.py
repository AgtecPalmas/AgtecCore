from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


class BaseApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(
            "test", email="testuser@test.com", password="test"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def setUp(self):
        self.client.login(username="test", password="test")

    def get_url_lista(self, app, modelo):
        return self.get_url_criar(app, modelo)

    def get_url_criar(self, app, modelo):
        return "/core/api/{0}/{1}/?format=json".format(app, modelo)

    def get_url_atualizar_excluir(self, app, modelo, pk):
        return "/core/api/{0}/{1}/{2}/?format=json".format(app, modelo, pk)

    def get_url_custom(self, app, modelo, metodo):
        return "/core/api/{0}/{1}/{2}/?format=json".format(app, modelo, metodo)
