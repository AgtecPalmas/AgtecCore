from authentication import use_cases, models, schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core import security
from core.config import settings
from core.database import get_db


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_str}/authentication/login"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
        )
    user = use_cases.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrador")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not use_cases.user.is_active(current_user):
        raise HTTPException(status_code=403, detail="Usuário inativo")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not use_cases.user.is_superuser(current_user):
        raise HTTPException(
            status_code=403, detail="O usuário não tem privilégios suficientes"
        )
    return current_user


def has_permission(permission_name: str):
    def has_permission_(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_active_user),
    ):
        app, codename = permission_name.split(".")
        if not current_user.is_superuser:
            permission = (
                db.query(models.Permission.id)
                .join(models.Group, models.User.groups)
                .join(models.Permission, models.Group.permissions)
                .join(models.ContentType, models.Permission.contentType)
                .filter(models.Permission.codename == codename)
                .filter(models.ContentType.app_label == app)
                .filter(models.User.id == current_user.id)
                .first()
            )
            if not permission:
                raise HTTPException(status_code=403, detail="Voce não tem permissao")
        return True

    return has_permission_
