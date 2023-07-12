# Django Rest Framework

## Sobre

Framework utilizado para criar APIs seguindo o padrão Rest.

## Settings

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ]
```

Configurando a estrutura de paginação dos responses, caso deseje alterar a quantidade de itens por página, basta alterar
o valor da chave **PAGE_SIZE**

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
    }
```

Configurando o padrão de filtros da API

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        ],
    }
```

Configurando quais formas de autenticação serão aceitas para consumir os endpoints

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    }
```

Configurando o padrão do parser, **deixar o padrão**

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_rapidjson.renderers.RapidJSONRenderer',
        ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_rapidjson.parsers.RapidJSONParser',
        ),
    }
```

------

## Exemplo completo da configuração padrão do projeto

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
    }
```

## Serializer(s)

Exemplo de serializer

```python
class UsuarioSerializer(ModelSerializer):
    """ Class do serializer do model Usuario para os métodos 
    POST, PUT, PATCH, DELETE """
    
    class Meta:
        model = Usuario
        fields = '__all__'


class UsuarioGETSerializer(FieldsListSerializerMixin, ModelSerializer):
    """ Class do serializer do model Usuario para o método GET """
    
    class Meta:
        model = Usuario
        fields = '__all__'
```

## View(s) - api_views.py

O decorator **@permission_classes([IsAuthenticated, ])** determina que os endpoints só podem ser acessados por usuários 
que estejam autenticados.

```python


@permission_classes([IsAuthenticated, ])
class UsuarioViewAPI(ModelViewSet):
    """ Classe para gerenciar as requisições da API para os métodos 
    POST, PUT, PATCH e DELETE """
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioSerializer


@permission_classes([IsAuthenticated, ])
class UsuarioGETAPI(OptimizedQuerySetMixin, ReadOnlyModelViewSet):
    """ Classe para gerenciar as requisições da API para o métodos GET

        A lista filterset_fields deve ser configurada com os 
        campos do models que poderão ser utilizados para realizar
        filtros no models como por exemplo 
        nome_do_campo=valor_a_ser_filtrado

        A lista search_fields deve ser configurada com os campos 
        do models que poderão ser utilizados para realizar
        buscas no models como por exemplo search=valor_a_ser_pesquisado
    """
    queryset = Usuario.objects.select_related().all()
    serializer_class = UsuarioGETSerializer
    filter_backend = [filters.SearchFilter]
    filterset_fields = []
    search_fields = []

```

## Url API - api_urls.py

```python
from .api_views import UsuarioViewAPI, UsuarioGETAPI

router = routers.DefaultRouter()

# URL para a API Usuario
# Configurando rota para o endpoint dos métodos POST PUT PATCH DELETE
router.register(r'usuario', UsuarioViewAPI, 'usuario-api')

# Configurando rota para o endpoint do método GET
router.register(r'usuario-get', UsuarioGETAPI, 'usuario-get-api')

urlpatterns = router.urls
```

## Url - urls.py

Para que as rotas sejam identificadas pela respectiva app é necessário adicionar o path abaixo no arquivo **urls.py** da
app

```python
path('api/usuario/', include('usuario.api_urls')),
```

## Links

|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/djangorestframework/)|[Doc](https://www.django-rest-framework.org/)|


