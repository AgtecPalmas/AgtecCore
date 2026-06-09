from django.urls import path

from usuario.views.usuario import (
    UsuarioLoginView,
    UsuarioLogoutView,
    UsuarioProfileView,
)

app_name = "usuario"

# URLs do Models Usuario
urlpatterns = [
    path("usuario/login/", UsuarioLoginView.as_view(), name="login"),
    path("usuario/userlogout/", UsuarioLogoutView.as_view(), name="logout"),
    path("usuario/userprofile/", UsuarioProfileView.as_view(), name="profile"),
]
