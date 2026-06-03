# Django User

A classe Usuario possui um relacionamento um para um com a classe User, esse relacionamento tem um campo chamado django_user.

Na geração do projeto FastAPI, algumas mudanças devem ser feitas para que nos endpoints de consulta, em fez de trazer o objeto do django_user, deve ser retornado a url com os dados do django_user daquele usuario.

Para isso, siga os passos abaixo:

### 1° Passo

No arquivo **schemas.py**, a classe **UsuarioBase** tem o campo *django_user* do tipo **User**. 
Deve-se trocar esse tipo para **str**.

Antes
```
django_user: Optional[User]
```

Depois
```
django_user: Optional[str]
```

### 2° Passo

No arquivo api.py, troque os métodos chamados.

Antes
```
def read_usuarios(db: Session = Depends(get_db), skip: int = 0, limit: int = 25) -> Any:
    """
    Retrieve usuarios.
    """
    usuarios = cruds.usuario.get_multi(db, skip=skip, limit=limit)
    for usuario in usuarios:
        usuario.django_user = crud_auth.user.get_by_id(db=db, id=usuario.django_user_id)
    return usuarios

def read_usuario_by_id(usuario_id: str, db: Session = Depends(get_db)) -> Any:
    """
    Get a specific usuario by id.
    """
    usuario = cruds.usuario.get(db, id=usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Item usuario inexistente no sistema")
    usuario.django_user = crud_auth.user.get_by_id(db=db, id=usuario.django_user_id)
    return usuario
```

Depois
```
def read_usuarios(request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 25) -> Any:
    """
    Retrieve usuarios.
    """
    usuarios = cruds.usuario.get_multi_paginate_django_user(
        db, request=request, offset=skip, limit=limit)
    return usuarios

def read_usuario_by_id(usuario_id: str, request: Request, db: Session = Depends(get_db)) -> Any:
    """
    Get a specific usuario by id.
    """
    usuario = cruds.usuario.get_paginate_django_user(
        db, request=request, id=usuario_id)
    return usuario
```