from drf_jsonmask.views import OptimizedQuerySetMixin
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from usuario.models import Usuario

from .serializers import UsuarioGETSerializer, UsuarioSerializer


class UsuarioViewAPI(ModelViewSet):
    """Classe para gerenciar as requisições da API para POST, PUT, PATCH e DELETE"""

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioSerializer


class UsuarioCustomViewAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
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
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []
