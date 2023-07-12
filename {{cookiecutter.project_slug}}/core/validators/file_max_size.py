from typing import Union

from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileMaxSizeValidator:
    """Define o tamanho máximo do arquivo em MB"""

    MB_TO_BYTES: int = 1024 * 1024

    def __init__(self, max_size: Union[float, int] = 1):
        if max_size <= 0:
            raise ValueError("O tamanho para validação do arquivo deve ser maior que 0")

        self.max_size = max_size

    def __call__(self, file):
        """Valida o tamanho do arquivo"""
        file_size = getattr(file, "size", 0)

        if file_size and file_size > self.max_size * self.MB_TO_BYTES:
            raise ValidationError(f"O tamanho máximo do arquivo é de {self.max_size}MB")

    def __repr__(self):
        """Retorna uma representação do objeto"""
        return f"FileMaxSizeValidator(max_size={self.max_size})"
