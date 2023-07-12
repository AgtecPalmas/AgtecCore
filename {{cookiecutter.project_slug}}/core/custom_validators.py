from django.core.exceptions import ValidationError


def tamanho_cpf(value):
    """
    Validador para o campo CPF
    """
    if len(value) > 14:
        raise ValidationError(
            "O campo CPF não pode ser superior a 14 caracteres", params={"value": value}
        )
