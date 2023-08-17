from django.urls import path

from .views import (
    UsuarioCreateView,
    UsuarioDeleteView,
    UsuarioDetailView,
    UsuarioIndexTemplateView,
    UsuarioListView,
    UsuarioLoginView,
    UsuarioLogoutView,
    UsuarioProfileView,
    UsuarioRestoreView,
    UsuarioUpdateView,
)

app_name = "usuario"

# URLs do Models Usuario
urlpatterns = [
    path("usuario/login/", UsuarioLoginView.as_view(), name="login"),
    path("usuario/userlogout/", UsuarioLogoutView.as_view(), name="logout"),
    path("usuario/userprofile/", UsuarioProfileView.as_view(), name="profile"),
]


# URLs do Models Usuario
urlpatterns += [
    path("usuario/", UsuarioIndexTemplateView.as_view(), name="usuario-index"),
    path("usuario/usuario/", UsuarioListView.as_view(), name="usuario-list"),
    path("usuario/usuario/create/", UsuarioCreateView.as_view(), name="usuario-create"),
    path(
        "usuario/usuario/<uuid:pk>/", UsuarioDetailView.as_view(), name="usuario-detail"
    ),
    path(
        "usuario/usuario/update/<uuid:pk>/",
        UsuarioUpdateView.as_view(),
        name="usuario-update",
    ),
    path(
        "usuario/usuario/delete/<uuid:pk>/",
        UsuarioDeleteView.as_view(),
        name="usuario-delete",
    ),
    path(
        "usuario/usuario/restore/<uuid:pk>/",
        UsuarioRestoreView.as_view(),
        name="usuario-restore",
    ),
]
