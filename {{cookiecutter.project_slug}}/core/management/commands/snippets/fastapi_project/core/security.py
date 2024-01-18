from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(
    default="django_pbkdf2_sha256",
    schemes=[
        "django_argon2",
        "django_bcrypt",
        "django_bcrypt_sha256",
        "django_pbkdf2_sha256",
        "django_pbkdf2_sha1",
        "django_disabled",
    ],
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1
ACCESS_REFRESHTOKEN_EXPIRE_MINUTES = 60 * 24 * 2

"""
Arquivo de configuração de segurança dos tokens JWT

- Métodos de verificação e criação de hash de senha
- Método para criar o token jwt válido
"""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_REFRESHTOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt
