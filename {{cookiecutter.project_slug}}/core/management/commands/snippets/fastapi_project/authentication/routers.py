from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr

from authentication import schemas, security, use_cases
from core.database import AsyncDBDependency
from core.security import create_access_token

router_user = APIRouter(prefix="/users", tags=["users"])


@router_user.get(
    "/",
    response_model=List[schemas.User],
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def fetch(db: AsyncDBDependency, skip: int = 0, limit: int = 25) -> Any:
    return await use_cases.user.get_multi(db, skip=skip, limit=limit)


@router_user.post("/", response_model=schemas.User)
async def create(*, db: AsyncDBDependency, user_in: schemas.UserCreate) -> Any:
    if use_cases.user.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=403,
            detail="The user with this username already exists in the system.",
        )
    return await use_cases.user.create(db, obj_in=user_in)


@router_user.get(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def get(user_id: int, db: AsyncDBDependency) -> Any:
    user = await use_cases.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


@router_user.put(
    "/{user_id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def update(
    *, db: AsyncDBDependency, user_id: int, user_in: schemas.UserUpdate
) -> Any:
    user = await use_cases.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = await use_cases.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router_user.delete(
    "/{id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def delete(*, db: AsyncDBDependency, id: int) -> Any:
    user = await use_cases.user.get(db=db, id=id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = await use_cases.user.delete(db=db, id=id)
    return user


router_auth = APIRouter(tags=["auth"])


@router_auth.post("/login", response_model=schemas.UserToken)
async def login_access_token(
    db: AsyncDBDependency, form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await use_cases.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=403, detail="Incorrect email or password")
    elif not use_cases.user.is_active(user):
        raise HTTPException(status_code=403, detail="Inactive user")
    return {
        **user.__dict__,
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router_auth.get("/profile", response_model=schemas.User)
def read_current_user(
    current_user: schemas.User = security.ACTIVE_USER_DEPENDENCY,
) -> Any:
    return current_user


@router_auth.put("/profile", response_model=schemas.User)
async def update_current_user(
    *,
    db: AsyncDBDependency,
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: schemas.User = security.ACTIVE_USER_DEPENDENCY,
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if email is not None:
        user_in.email = email
    return await use_cases.user.update(db, db_obj=current_user, obj_in=user_in)


router_permission = APIRouter(
    prefix="/permisions",
    tags=["permisions"],
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)


@router_permission.get(
    "/",
    response_model=List[schemas.Permission],
    dependencies=[Depends(security.has_permission("authentication.permission_view"))],
)
async def fetch(db: AsyncDBDependency, skip: int = 0, limit: int = 25) -> Any:
    return await use_cases.permission.get_multi(db, skip=skip, limit=limit)


@router_permission.post("/", response_model=schemas.Permission)
async def create(
    *, db: AsyncDBDependency, permission_in: schemas.PermissionCreate
) -> Any:
    return await use_cases.permission.create(db, obj_in=permission_in)


@router_permission.get("/{permission_id}", response_model=schemas.Permission)
async def get(permission_id: int, db: AsyncDBDependency) -> Any:
    return await use_cases.permission.get(db, id=permission_id)


@router_permission.put("/{permission_id}", response_model=schemas.Permission)
async def update(
    *,
    db: AsyncDBDependency,
    permission_id: int,
    permission_in: schemas.PermissionUpdate,
) -> Any:
    permission = await use_cases.permission.get(db, id=permission_id)
    return await use_cases.permission.update(
        db, db_obj=permission, obj_in=permission_in
    )


@router_permission.delete("/{id}", response_model=schemas.Permission)
async def delete(*, db: AsyncDBDependency, id: int) -> Any:
    await use_cases.permission.get(db=db, id=id)
    return await use_cases.permission.delete(db=db, id=id)


router_group = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)


@router_group.get("/", response_model=List[schemas.Group])
async def fetch(db: AsyncDBDependency, skip: int = 0, limit: int = 25) -> Any:
    return await use_cases.group.get_multi(db, skip=skip, limit=limit)


@router_group.post("/", response_model=schemas.Group)
async def create(*, db: AsyncDBDependency, group_in: schemas.GroupCreate) -> Any:
    return await use_cases.group.create(db, obj_in=group_in)


@router_group.get("/{group_id}", response_model=schemas.Group)
async def get(group_id: int, db: AsyncDBDependency) -> Any:
    return await use_cases.group.get(db, id=group_id)


@router_group.put("/{group_id}", response_model=schemas.Group)
async def update(
    *, db: AsyncDBDependency, group_id: int, group_in: schemas.GroupUpdate
) -> Any:
    group = await use_cases.group.get(db, id=group_id)
    return await use_cases.group.update(db, db_obj=group, obj_in=group_in)


@router_group.delete("/{id}", response_model=schemas.Group)
async def delete(*, db: AsyncDBDependency, id: int) -> Any:
    await use_cases.group.get(db=db, id=id)
    return use_cases.group.delete(db=db, id=id)


router = APIRouter()
router.include_router(router_user)
router.include_router(router_auth)
router.include_router(router_permission)
router.include_router(router_group)
