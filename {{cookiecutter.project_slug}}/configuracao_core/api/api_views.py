from drf_jsonmask.views import OptimizedQuerySetMixin
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from configuracao_core.models import (
    DadosGerais,
    Gestor,
    ImagemGenerica,
    ImagemLogin,
    ImagensSistema,
    LogoSistema,
    RedeSocial,
)

from .serializers import (
    DadosGeraisGETSerializer,
    DadosGeraisSerializer,
    GestorGETSerializer,
    GestorSerializer,
    ImagemGenericaGETSerializer,
    ImagemGenericaSerializer,
    ImagemLoginGETSerializer,
    ImagemLoginSerializer,
    ImagensSistemaGETSerializer,
    ImagensSistemaSerializer,
    LogoSistemaGETSerializer,
    LogoSistemaSerializer,
    RedeSocialGETSerializer,
    RedeSocialSerializer,
)


class GestorViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Gestor.objects.select_related().all()
    serializer_class = GestorSerializer


class GestorCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = Gestor.objects.select_related().all()
    serializer_class = GestorGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class ImagemLoginViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ImagemLogin.objects.select_related().all()
    serializer_class = ImagemLoginSerializer


class ImagemLoginCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = ImagemLogin.objects.select_related().all()
    serializer_class = ImagemLoginGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class LogoSistemaViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = LogoSistema.objects.select_related().all()
    serializer_class = LogoSistemaSerializer


class LogoSistemaCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = LogoSistema.objects.select_related().all()
    serializer_class = LogoSistemaGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class DadosGeraisViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DadosGerais.objects.select_related().all()
    serializer_class = DadosGeraisSerializer


class DadosGeraisCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = DadosGerais.objects.select_related().all()
    serializer_class = DadosGeraisGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class RedeSocialViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = RedeSocial.objects.select_related().all()
    serializer_class = RedeSocialSerializer


class RedeSocialCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = RedeSocial.objects.select_related().all()
    serializer_class = RedeSocialGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class ImagemGenericaViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ImagemGenerica.objects.select_related().all()
    serializer_class = ImagemGenericaSerializer


class ImagemGenericaCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = ImagemGenerica.objects.select_related().all()
    serializer_class = ImagemGenericaGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []


class ImagensSistemaViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ImagensSistema.objects.select_related().all()
    serializer_class = ImagensSistemaSerializer


class ImagensSistemaCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """Classe para gerenciar as requisições da API para o GET

    A lista filterset_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    filtros no models como por exemplo nome_do_campo=valor_a_ser_filtrado

    A lista search_fields deve ser configurada com os campos do models que poderão ser utilizados para realizar
    buscas no models como por exemplo search=valor_a_ser_pesquisado
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = ImagensSistema.objects.select_related().all()
    serializer_class = ImagensSistemaGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []
