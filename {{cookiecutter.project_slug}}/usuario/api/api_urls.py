from rest_framework import routers

from .api_views import UsuarioCustomViewAPI, UsuarioViewAPI

router = routers.DefaultRouter()

# URL para a API Usuario
router.register(r"usuario", UsuarioViewAPI, "usuario-api")
router.register(r"usuario/custom", UsuarioCustomViewAPI, "usuario-get-api")

urlpatterns = router.urls
