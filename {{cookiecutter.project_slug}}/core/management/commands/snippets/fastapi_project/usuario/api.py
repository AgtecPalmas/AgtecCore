import json
from typing import Any, List

import requests
from authentication import cruds as crud_auth
from authentication import security
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db

from . import cruds, schemas

router = APIRouter()

router_usuario = APIRouter(
    prefix="/usuario",
    tags=["usuario"],
    dependencies=[Depends(security.get_current_active_user)],
)


@router_usuario.get(
    "/",
    response_model=List[schemas.Usuario],
    dependencies=[Depends(security.has_permission("usuario.view_usuario"))],
)
def read_usuarios(db: Session = Depends(get_db), skip: int = 0, limit: int = 25) -> Any:
    """
    Retrieve usuarios.
    """
    usuarios = cruds.usuario.get_multi(db, skip=skip, limit=limit)
    for usuario in usuarios:
        usuario.django_user = crud_auth.user.get_by_id(db=db, id=usuario.django_user_id)
    return usuarios


@router_usuario.post(
    "/",
    response_model=schemas.Usuario,
    dependencies=[Depends(security.has_permission("usuario.add_usuario"))],
)
def create_usuario(
    *, db: Session = Depends(get_db), usuario_in: schemas.UsuarioCreate
) -> Any:
    """
    Create new usuario.
    """
    # Request ao Django REST
    response = requests.post(
        f"{settings.django_url}/usuario/api/v1/usuario/?format=json",
        json=usuario_in.dict(),
    )

    # 201 é criado com sucesso
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao criar usuario no django: {response.text}",
        )

    response_data = json.loads(response.text)

    # Atualiza o usuario com o id do django
    cruds.usuario.update(
        db,
        db_obj=cruds.usuario.get(db, id=response_data.get("id")),
        obj_in=schemas.UsuarioUpdate(
            django_user_id=response_data.get("django_user"),
            nome=usuario_in.nome,
            email=usuario_in.email,
        ),
    )

    usuario = cruds.usuario.get(db, id=response_data.get("id"))
    return usuario


@router_usuario.get(
    "/{usuario_id}",
    response_model=schemas.Usuario,
    dependencies=[Depends(security.has_permission("usuario.view_usuario"))],
)
def read_usuario_by_id(usuario_id: str, db: Session = Depends(get_db)) -> Any:
    """
    Get a specific usuario by id.
    """
    usuario = cruds.usuario.get(db, id=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=404, detail="Item usuario inexistente no sistema"
        )
    usuario.django_user = crud_auth.user.get_by_id(db=db, id=usuario.django_user_id)
    return usuario


@router_usuario.put(
    "/{usuario_id}",
    response_model=schemas.Usuario,
    dependencies=[Depends(security.has_permission("usuario.change_usuario"))],
)
def update_usuario(
    *,
    db: Session = Depends(get_db),
    usuario_id: str,
    usuario_in: schemas.UsuarioUpdate,
) -> Any:
    """
    Update a usuario.
    """
    usuario = cruds.usuario.get(db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario inexistente no sistema")
    usuario = cruds.usuario.update(db, db_obj=usuario, obj_in=usuario_in)
    return usuario


@router_usuario.delete(
    "/{id}",
    response_model=schemas.Usuario,
    dependencies=[Depends(security.has_permission("usuario.delete_usuario"))],
)
def delete_usuario(*, db: Session = Depends(get_db), id: str) -> Any:
    """
    Delete a usuario.
    """
    usuario = cruds.usuario.get(db=db, id=id)
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario inexistente no sistema")
    usuario = cruds.usuario.remove(db=db, id=id)
    return usuario


router.include_router(router_usuario)
