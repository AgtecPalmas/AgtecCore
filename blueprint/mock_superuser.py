import os

import django
from decouple import config
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from django.contrib.auth.models import User


class Mock:
    @staticmethod
    def create_superuser():
        try:
            User.objects.create_superuser(
                username="admin",
                email="email@email.com.br",
                password=config("SENHA_PADRAO"),
            )
            print("✅ Superuser Admin criado")

        except IntegrityError:
            print("⚠️  Usuário admin já existe")

        except Exception as error:
            print(f"💥 {error}")


if __name__ == "__main__":
    Mock().create_superuser()
