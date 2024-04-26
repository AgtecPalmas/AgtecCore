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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views.base import BaseIndexTemplate
from core.views.errors import (
    BadRequestView,
    PageNotFoundView,
    PermissionDeniedView,
    ServerErrorView,
)

from . import urls_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BaseIndexTemplate.as_view(), name="index"),
    path("core/", include("core.urls", namespace="core")),
    # Urls do Swagger
    path("swagger/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Url de autenticação do DRF
    path("auth/", include("dj_rest_auth.urls")),
    # URL de autenticação JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("select2/", include("django_select2.urls")),
]

# Adicionando as urls da APIRest no urlpatterns do projeto
urlpatterns += urls_api.urlpatterns

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

handler400 = BadRequestView.as_view()
handler403 = PermissionDeniedView.as_view()
handler404 = PageNotFoundView.as_view()
handler500 = ServerErrorView.as_view()
