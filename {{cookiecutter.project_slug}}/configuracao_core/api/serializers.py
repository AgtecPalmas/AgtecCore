from drf_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework.serializers import ModelSerializer

from configuracao_core.models import (
    DadosGerais,
    Gestor,
    ImagemGenerica,
    ImagemLogin,
    ImagensSistema,
    LogoSistema,
    RedeSocial,
)


class GestorSerializer(ModelSerializer):
    """Class do serializer do model Gestor para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = Gestor
        exclude = ["deleted", "enabled"]


class GestorGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model Gestor para o GET"""

    class Meta:
        model = Gestor
        exclude = ["deleted", "enabled"]


class ImagemLoginSerializer(ModelSerializer):
    """Class do serializer do model ImagemLogin para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = ImagemLogin
        exclude = ["deleted", "enabled"]


class ImagemLoginGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model ImagemLogin para o GET"""

    class Meta:
        model = ImagemLogin
        exclude = ["deleted", "enabled"]


class LogoSistemaSerializer(ModelSerializer):
    """Class do serializer do model LogoSistema para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = LogoSistema
        exclude = ["deleted", "enabled"]


class LogoSistemaGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model LogoSistema para o GET"""

    class Meta:
        model = LogoSistema
        exclude = ["deleted", "enabled"]


class DadosGeraisSerializer(ModelSerializer):
    """Class do serializer do model DadosGerais para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = DadosGerais
        exclude = ["deleted", "enabled"]


class DadosGeraisGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model DadosGerais para o GET"""

    class Meta:
        model = DadosGerais
        exclude = ["deleted", "enabled"]


class RedeSocialSerializer(ModelSerializer):
    """Class do serializer do model RedeSocial para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = RedeSocial
        exclude = ["deleted", "enabled"]


class RedeSocialGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model RedeSocial para o GET"""

    class Meta:
        model = RedeSocial
        exclude = ["deleted", "enabled"]


class ImagemGenericaSerializer(ModelSerializer):
    """Class do serializer do model ImagemGenerica para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = ImagemGenerica
        exclude = ["deleted", "enabled"]


class ImagemGenericaGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model ImagemGenerica para o GET"""

    class Meta:
        model = ImagemGenerica
        exclude = ["deleted", "enabled"]


class ImagensSistemaSerializer(ModelSerializer):
    """Class do serializer do model ImagensSistema para o POST, PUT, PATCH, DELETE"""

    class Meta:
        model = ImagensSistema
        exclude = ["deleted", "enabled"]


class ImagensSistemaGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """Class do serializer do model ImagensSistema para o GET"""

    class Meta:
        model = ImagensSistema
        exclude = ["deleted", "enabled"]
