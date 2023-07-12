from authentication.api import router as router_users
from fastapi import APIRouter

from usuario.api import router as router_usuario_usuario

from .config import settings

"""
TODO Importar para esse arquivo os endpoints das apps do Projeto
Arquivos com os endpoints principais do projeto

- Deve ser importado nesse arquivo, os arquivo routers de todas as apps
"""

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(router_users, prefix="/authentication")
api_router.include_router(router_usuario_usuario, prefix="/usuario")
