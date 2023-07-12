from typing import Any, List

from authentication import cruds, schemas, security
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import create_access_token

"""
Arquivos com os endpoints da app

- Crud completo de usuários, grupos e permissões
- Login
- Atualização de perfil
- Validação de endpoints com usuário logado ou permissões
"""

router_user = APIRouter(prefix="/users", tags=["users"])


@router_user.get(
    "/",
    response_model=List[schemas.User],
    dependencies=[Depends(security.get_current_active_user)],
)
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 25) -> Any:
    users = cruds.user.get_multi(db, skip=skip, limit=limit)
    return users


@router_user.post("/", response_model=schemas.User)
def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate) -> Any:
    user = cruds.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=403,
            detail="The user with this username already exists in the system.",
        )
    user = cruds.user.create(db, obj_in=user_in)
    return user


@router_user.get(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(security.get_current_active_user)],
)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)) -> Any:
    user = cruds.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


@router_user.put(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(security.get_current_active_user)],
)
def update_user(
    *, db: Session = Depends(get_db), user_id: int, user_in: schemas.UserUpdate
) -> Any:
    user = cruds.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = cruds.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router_user.delete(
    "/{id}",
    response_model=schemas.User,
    dependencies=[Depends(security.get_current_active_user)],
)
def delete_note(*, db: Session = Depends(get_db), id: int) -> Any:
    user = cruds.user.get(db=db, id=id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = cruds.user.remove(db=db, id=id)
    return user


router_auth = APIRouter(tags=["auth"])


@router_auth.post("/login", response_model=schemas.UserToken)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = cruds.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    elif not cruds.user.is_active(user):
        raise HTTPException(status_code=403, detail="Inactive user")
    return {
        **user.__dict__,
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router_auth.get("/profile", response_model=schemas.User)
def read_user_me(
    current_user: schemas.User = Depends(security.get_current_active_user),
) -> Any:
    return current_user


@router_auth.put("/profile", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: schemas.User = Depends(security.get_current_active_user)
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if email is not None:
        user_in.email = email
    user = cruds.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


router_permission = APIRouter(
    prefix="/permisions",
    tags=["permisions"],
    dependencies=[Depends(security.get_current_active_user)],
)


@router_permission.get(
    "/",
    response_model=List[schemas.Permission],
    dependencies=[Depends(security.has_permission("authentication.permission_view"))],
)
def read_permissions(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 25
) -> Any:
    permissions = cruds.permission.get_multi(db, skip=skip, limit=limit)
    return permissions


@router_permission.post("/", response_model=schemas.Permission)
def create_permission(
    *, db: Session = Depends(get_db), permission_in: schemas.PermissionCreate
) -> Any:
    permission = cruds.permission.create(db, obj_in=permission_in)
    return permission


@router_permission.get("/{permission_id}", response_model=schemas.Permission)
def read_permission_by_id(permission_id: int, db: Session = Depends(get_db)) -> Any:
    permission = cruds.permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404, detail="The permission does not exist in the system"
        )
    return permission


@router_permission.put("/{permission_id}", response_model=schemas.Permission)
def update_permission(
    *,
    db: Session = Depends(get_db),
    permission_id: int,
    permission_in: schemas.PermissionUpdate
) -> Any:
    permission = cruds.permission.get(db, id=permission_id)
    if not permission:
        raise HTTPException(
            status_code=404, detail="The permission does not exist in the system"
        )
    permission = cruds.permission.update(db, db_obj=permission, obj_in=permission_in)
    return permission


@router_permission.delete("/{id}", response_model=schemas.Permission)
def delete_permission(*, db: Session = Depends(get_db), id: int) -> Any:
    permission = cruds.permission.get(db=db, id=id)
    if not permission:
        raise HTTPException(
            status_code=404, detail="The permission does not exist in the system"
        )
    permission = cruds.permission.remove(db=db, id=id)
    return permission


router_group = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[Depends(security.get_current_active_user)],
)


@router_group.get("/", response_model=List[schemas.Group])
def read_groups(db: Session = Depends(get_db), skip: int = 0, limit: int = 25) -> Any:
    groups = cruds.group.get_multi(db, skip=skip, limit=limit)
    return groups


@router_group.post("/", response_model=schemas.Group)
def create_group(
    *, db: Session = Depends(get_db), group_in: schemas.GroupCreate
) -> Any:
    group = cruds.group.create(db, obj_in=group_in)
    return group


@router_group.get("/{group_id}", response_model=schemas.Group)
def read_group_by_id(group_id: int, db: Session = Depends(get_db)) -> Any:
    group = cruds.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404, detail="The group does not exist in the system"
        )
    return group


@router_group.put("/{group_id}", response_model=schemas.Group)
def update_group(
    *, db: Session = Depends(get_db), group_id: int, group_in: schemas.GroupUpdate
) -> Any:
    group = cruds.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404, detail="The group does not exist in the system"
        )
    group = cruds.group.update(db, db_obj=group, obj_in=group_in)
    return group


@router_group.delete("/{id}", response_model=schemas.Group)
def delete_note(*, db: Session = Depends(get_db), id: int) -> Any:
    group = cruds.group.get(db=db, id=id)
    if not group:
        raise HTTPException(
            status_code=404, detail="The group does not exist in the system"
        )
    group = cruds.group.remove(db=db, id=id)
    return group


router = APIRouter()
router.include_router(router_user)
router.include_router(router_auth)
router.include_router(router_permission)
router.include_router(router_group)
