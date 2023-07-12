"""{{ cookiecutter.project_slug }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from core.views.base import BaseIndexTemplate
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import urls_api

schema_view = get_schema_view(
    openapi.Info(
        title="{{ cookiecutter.project_name }} API",
        default_version="v1",
        description="Swagger do Projeto {{ cookiecutter.project_name.title() }} API",
        terms_of_service="https://www.{{ cookiecutter.domain_name }}/",
        contact=openapi.Contact(email="{{ cookiecutter.email }}"),
        license=openapi.License(name="BSD License"),
    ),
    url="http://127.0.0.1:8000"
    if settings.DEBUG
    else "https://www.{{ cookiecutter.domain_name }}",
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BaseIndexTemplate.as_view(), name="index"),
    path("core/", include("core.urls", namespace="core")),
    # Urls do Swagger
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Url de autenticação do DRF
    path("auth/", include("dj_rest_auth.urls")),
    # URL de autenticação JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Adicionando as urls da APIRest no urlpatterns do projeto
urlpatterns += urls_api.urlpatterns

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
