import contextlib
import re
import uuid
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.db.models import Q

from core.excecoes import CpfCnpjValidationError

cache = caches[getattr(settings, "CACHE_NAME", DEFAULT_CACHE_ALIAS)]

# Validators
EMPTY_VALUES = (None, "", [], (), {})


def obter_modelo(nome_modelo):
    if not nome_modelo:
        return None
    try:
        return next(
            (
                m
                for m in apps.get_models()
                if m._meta.model_name.lower() == nome_modelo.lower()
            ),
            None,
        )
    except LookupError:
        return None


def registro_existente(objeto, campo):
    campo_str = "{0}__iexact".format(campo)
    filtro = Q(**{campo_str: getattr(objeto, campo)})
    if objeto.id:
        return objeto._meta.model.objects.exclude(id=objeto.id).filter(filtro).exists()
    else:
        return objeto._meta.model.objects.filter(filtro).exists()


def DV_maker(v):
    return 11 - v if v >= 2 else 0


def is_valid_cpf(value):
    error_messages = {
        "invalid": "CPF Inválido",
        "max_digits": (
            "CPF possui 11 dígitos (somente números) ou 14" " (com pontos e hífen)"
        ),
        "digits_only": ("Digite um CPF com apenas números ou com ponto e " "hífen"),
    }

    if value in EMPTY_VALUES:
        return ""
    orig_value = value[:]
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    try:
        int(value)
    except ValueError as e:
        raise CpfCnpjValidationError(error_messages["digits_only"]) from e
    if len(value) != 11:
        raise CpfCnpjValidationError(error_messages["max_digits"])
    orig_dv = value[-2:]

    new_1dv = sum(i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1)))
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum(i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1)))
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise CpfCnpjValidationError(error_messages["invalid"])

    return orig_value


def limpar_espacos_duplos(text: str) -> str:
    """Remove espaços duplos"""
    return re.sub(r"\s+", " ", text)


def limpar_chars_especiais(text: str) -> str:
    """Remove caracteres especiais mas deixa acentos"""
    return re.sub(r"[^a-zA-ZÀ-ú ]", "", text)


def somente_numeros(text: str) -> str:
    """Retorna string somente com números"""
    return re.sub(r"[^0-9]", "", text)


def somente_letras(text: str) -> str:
    """Retorna string somente com letras e acentos"""
    text: str = limpar_espacos_duplos(text)
    return limpar_chars_especiais(text).strip()


def somente_letras_numeros(text: str) -> str:
    """Retorna string somente com letras, acentos, números e espaços"""
    text: str = limpar_espacos_duplos(text)
    return re.sub(r"[^a-zA-ZÀ-ú0-9 ]", "", text)


def save_to_cache(key: str, value, time: int = 300) -> None:
    """Salva o token no cache"""
    cache.set(key, value, time)


def get_cache(key: str) -> str:
    """Retorna o valor do cache"""
    return cache.get(key)


def save_file_to(instance, filename) -> str:
    """Salva o arquivo no diretório da app/model com um nome único"""
    return "".join(
        [
            instance._meta.app_label,
            "/",
            instance._meta.model_name,
            "/",
            str(uuid.uuid4()),
            Path(filename).suffix,
        ]
    )


def get_full_url_static(file: str) -> str:
    """Retorna o caminho completo do arquivo estático"""
    return staticfiles_storage.url(file)
