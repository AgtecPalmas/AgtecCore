from core.cruds import CRUDBase

from .models import Usuario
from .schemas import UsuarioCreate, UsuarioUpdate


class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):
    pass


usuario = CRUDUsuario(Usuario)
