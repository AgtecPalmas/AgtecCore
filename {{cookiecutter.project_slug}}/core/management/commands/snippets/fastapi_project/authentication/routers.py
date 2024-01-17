from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.networks import EmailStr

from authentication import schemas, security, use_cases
from core.database import AsyncDBDependency
from core.schemas import PaginationBase
from core.security import create_access_token

router_user = APIRouter(prefix="/users", tags=["users"])


@router_user.get(
    "/",
    response_model=PaginationBase,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def fetch(
    db: AsyncDBDependency, request: Request, offset: int = 0, limit: int = 25
) -> Any:
    return await use_cases.user.get_paginate(
        db, request=request, offset=offset, limit=limit, model_pydantic=schemas.User
    )


@router_user.post("/", response_model=schemas.User)
async def create(db: AsyncDBDependency, data: schemas.UserCreate) -> Any:
    if await use_cases.user.get_by_username(db, username=data.username):
        raise HTTPException(
            status_code=403,
            detail="The user with this username already exists in the system.",
        )
    if await use_cases.user.get_by_email(db, email=data.email):
        raise HTTPException(
            status_code=403,
            detail="The user with this email already exists in the system.",
        )
    return await use_cases.user.create(db, data)


@router_user.get(
    "/{id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def get(db: AsyncDBDependency, id: int) -> Any:
    return await use_cases.user.get(db, id)


@router_user.put(
    "/{id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def update(db: AsyncDBDependency, id: int, data: schemas.UserUpdate) -> Any:
    item = await use_cases.user.get(db, id)
    return await use_cases.user.update(db, item, data)


@router_user.delete(
    "/{id}",
    response_model=schemas.User,
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)
async def delete(db: AsyncDBDependency, id: int) -> Any:
    await use_cases.user.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
    db: AsyncDBDependency,
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: schemas.User = security.ACTIVE_USER_DEPENDENCY,
) -> Any:
    if (
        email
        and await use_cases.user.get_by_email(db, email)
        and email != current_user.email
    ):
        raise HTTPException(
            status_code=403,
            detail="The user with this email already exists in the system.",
        )

    current_user.first_name = first_name or current_user.first_name
    current_user.last_name = last_name or current_user.last_name
    current_user.email = email or current_user.email

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


router_permission = APIRouter(
    prefix="/permisions",
    tags=["permisions"],
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)


@router_permission.get(
    "/",
    response_model=PaginationBase,
    dependencies=[Depends(security.has_permission("authentication.permission_view"))],
)
async def fetch(
    db: AsyncDBDependency, request: Request, offset: int = 0, limit: int = 25
) -> Any:
    return await use_cases.permission.get_paginate(
        db,
        request=request,
        offset=offset,
        limit=limit,
        model_pydantic=schemas.Permission,
    )


@router_permission.post("/", response_model=schemas.Permission)
async def create(db: AsyncDBDependency, data: schemas.PermissionCreate) -> Any:
    return await use_cases.permission.create(db, data)


@router_permission.get("/{id}", response_model=schemas.Permission)
async def get(db: AsyncDBDependency, id: int) -> Any:
    return await use_cases.permission.get(db, id)


@router_permission.put("/{id}", response_model=schemas.Permission)
async def update(
    db: AsyncDBDependency,
    id: int,
    data: schemas.PermissionUpdate,
) -> Any:
    item = await use_cases.permission.get(db, id)
    return await use_cases.permission.update(db, item, data)


@router_permission.delete("/{id}", response_model=schemas.Permission)
async def delete(db: AsyncDBDependency, id: int) -> Any:
    await use_cases.permission.get(db, id)
    await use_cases.permission.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


router_group = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[security.ACTIVE_USER_DEPENDENCY],
)


@router_group.get("/", response_model=PaginationBase)
async def fetch(
    db: AsyncDBDependency,
    request: Request,
    offset: int = 0,
    limit: int = 25,
) -> Any:
    return await use_cases.group.get_paginate(
        db, request=request, offset=offset, limit=limit, model_pydantic=schemas.Group
    )


@router_group.post("/", response_model=schemas.Group)
async def create(db: AsyncDBDependency, data: schemas.GroupCreate) -> Any:
    return await use_cases.group.create(db, data)


@router_group.get("/{id}", response_model=schemas.Group)
async def get(db: AsyncDBDependency, id: int) -> Any:
    return await use_cases.group.get(db, id)


@router_group.put("/{id}", response_model=schemas.Group)
async def update(db: AsyncDBDependency, id: int, data: schemas.GroupUpdate) -> Any:
    item = await use_cases.group.get(db, id)
    return await use_cases.group.update(db, item, data)


@router_group.delete("/{id}", response_model=schemas.Group)
async def delete(db: AsyncDBDependency, id: int) -> Any:
    await use_cases.group.get(db, id)
    await use_cases.group.delete(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


router = APIRouter()
router.include_router(router_user)
router.include_router(router_auth)
router.include_router(router_permission)
router.include_router(router_group)
