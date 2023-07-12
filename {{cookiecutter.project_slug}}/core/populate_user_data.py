"""Código para popular dados de exemplo do models User
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from faker import Faker
from validate_docbr import CPF
import random
from clientes.models import Cliente


def criando_pessoas(quantidade_de_pessoas):
    fake = Faker("pt_BR")
    Faker.seed(10)
    for _ in range(quantidade_de_pessoas):
        cpf = CPF()
        nome = fake.name()
        email = "{}@{}".format(nome.lower(), fake.free_email_domain())
        email = email.replace(" ", "")
        cpf = cpf.generate()
        rg = "{}{}{}{}".format(
            random.randrange(10, 99),
            random.randrange(100, 999),
            random.randrange(100, 999),
            random.randrange(0, 9),
        )
        celular = "{} 9{}-{}".format(
            random.randrange(10, 21),
            random.randrange(4000, 9999),
            random.randrange(4000, 9999),
        )
        ativo = random.choice([True, False])
        p = Cliente(
            nome=nome, email=email, cpf=cpf, rg=rg, celular=celular, ativo=ativo
        )
        p.save()


criando_pessoas(50)
