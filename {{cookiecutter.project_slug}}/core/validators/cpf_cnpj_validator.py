import re
from itertools import cycle

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class CPFCPNJValidator:
    """Valida CPF e CNPJ"""

    def __init__(self, tipo: str = "ambos"):
        self.validadores = {
            "ambos": [self.validate_cpf, self.validate_cnpj],
            "cpf": [self.validate_cpf],
            "cnpj": [self.validate_cnpj],
        }

        if tipo in self.validadores:
            self.validadores = self.validadores[tipo]

        else:
            raise ValueError("O tipo deve ser 'ambos', 'cpf' ou 'cnpj'")

    @staticmethod
    def clean(cpf_cnpj: str) -> str:
        """Remove caracteres especiais do CPF/CNPJ"""
        return re.sub(r"[^0-9]", "", cpf_cnpj)

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida CPF"""
        if len(cpf) != 11:
            return False

        if cpf in {s * 11 for s in [str(n) for n in range(10)]}:
            return False

        calc = lambda t: int(t[1]) * (t[0] + 2)
        d1 = (sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11
        d2 = (sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11
        return str(d1) == cpf[-2] and str(d2) == cpf[-1]

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Valida CNPJ"""
        if len(cnpj) != 14:
            return False

        if cnpj in {c * 14 for c in "1234567890"}:
            return False

        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1 : i] != str(dv % 10):
                return False

        return True

    def __call__(self, cpf_cnpj: str):
        """Valida CPF/CNPJ"""
        cpf_cnpj = self.clean(cpf_cnpj)

        if any(validator(cpf_cnpj) for validator in self.validadores):
            return

        raise ValidationError("CPF/CNPJ inválido")
