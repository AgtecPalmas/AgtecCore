from rest_framework import routers

from .api_views import (
    DadosGeraisCustomViewAPI,
    DadosGeraisViewAPI,
    GestorCustomViewAPI,
    GestorViewAPI,
    ImagemGenericaCustomViewAPI,
    ImagemGenericaViewAPI,
    ImagemLoginCustomViewAPI,
    ImagemLoginViewAPI,
    ImagensSistemaCustomViewAPI,
    ImagensSistemaViewAPI,
    LogoSistemaCustomViewAPI,
    LogoSistemaViewAPI,
    RedeSocialCustomViewAPI,
    RedeSocialViewAPI,
)

router = routers.DefaultRouter()

# URL para a API Gestor
router.register(r"gestor", GestorViewAPI, "gestor-api")
router.register(r"gestor/custom", GestorCustomViewAPI, "gestor-get-api")


# URL para a API ImagemLogin
router.register(r"imagemlogin", ImagemLoginViewAPI, "imagemlogin-api")
router.register(r"imagemlogin/custom", ImagemLoginCustomViewAPI, "imagemlogin-get-api")


# URL para a API LogoSistema
router.register(r"logosistema", LogoSistemaViewAPI, "logosistema-api")
router.register(r"logosistema/custom", LogoSistemaCustomViewAPI, "logosistema-get-api")


# URL para a API DadosGerais
router.register(r"dadosgerais", DadosGeraisViewAPI, "dadosgerais-api")
router.register(r"dadosgerais/custom", DadosGeraisCustomViewAPI, "dadosgerais-get-api")


# URL para a API RedeSocial
router.register(r"redesocial", RedeSocialViewAPI, "redesocial-api")
router.register(r"redesocial/custom", RedeSocialCustomViewAPI, "redesocial-get-api")


# URL para a API ImagemGenerica
router.register(r"imagemgenerica", ImagemGenericaViewAPI, "imagemgenerica-api")
router.register(
    r"imagemgenerica/custom", ImagemGenericaCustomViewAPI, "imagemgenerica-get-api"
)


# URL para a API ImagensSistema
router.register(r"imagenssistema", ImagensSistemaViewAPI, "imagenssistema-api")
router.register(
    r"imagenssistema/custom", ImagensSistemaCustomViewAPI, "imagenssistema-get-api"
)

urlpatterns = router.urls
