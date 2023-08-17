from django.urls import path

from .views import (
    Configuracao_CoreIndexTemplateView,
    DadosGeraisCreateView,
    DadosGeraisDeleteView,
    DadosGeraisDetailView,
    DadosGeraisListView,
    DadosGeraisRestoreView,
    DadosGeraisUpdateView,
    GestorCreateView,
    GestorDeleteView,
    GestorDetailView,
    GestorListView,
    GestorRestoreView,
    GestorUpdateView,
    ImagemGenericaCreateView,
    ImagemGenericaDeleteView,
    ImagemGenericaDetailView,
    ImagemGenericaListView,
    ImagemGenericaRestoreView,
    ImagemGenericaUpdateView,
    ImagemLoginCreateView,
    ImagemLoginDeleteView,
    ImagemLoginDetailView,
    ImagemLoginListView,
    ImagemLoginRestoreView,
    ImagemLoginUpdateView,
    ImagensSistemaCreateView,
    ImagensSistemaDeleteView,
    ImagensSistemaDetailView,
    ImagensSistemaListView,
    ImagensSistemaRestoreView,
    ImagensSistemaUpdateView,
    LogoSistemaCreateView,
    LogoSistemaDeleteView,
    LogoSistemaDetailView,
    LogoSistemaListView,
    LogoSistemaRestoreView,
    LogoSistemaUpdateView,
    RedeSocialCreateView,
    RedeSocialDeleteView,
    RedeSocialDetailView,
    RedeSocialListView,
    RedeSocialRestoreView,
    RedeSocialUpdateView,
)

app_name = "configuracao_core"

# URLs do Models Gestor
urlpatterns = [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path("configuracao_core/gestor/", GestorListView.as_view(), name="gestor-list"),
    path(
        "configuracao_core/gestor/create/",
        GestorCreateView.as_view(),
        name="gestor-create",
    ),
    path(
        "configuracao_core/gestor/<uuid:pk>/",
        GestorDetailView.as_view(),
        name="gestor-detail",
    ),
    path(
        "configuracao_core/gestor/update/<uuid:pk>/",
        GestorUpdateView.as_view(),
        name="gestor-update",
    ),
    path(
        "configuracao_core/gestor/delete/<uuid:pk>/",
        GestorDeleteView.as_view(),
        name="gestor-delete",
    ),
    path(
        "configuracao_core/gestor/restore/<uuid:pk>/",
        GestorRestoreView.as_view(),
        name="gestor-restore",
    ),
]


# URLs do Models ImagemLogin
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/imagemlogin/",
        ImagemLoginListView.as_view(),
        name="imagemlogin-list",
    ),
    path(
        "configuracao_core/imagemlogin/create/",
        ImagemLoginCreateView.as_view(),
        name="imagemlogin-create",
    ),
    path(
        "configuracao_core/imagemlogin/<uuid:pk>/",
        ImagemLoginDetailView.as_view(),
        name="imagemlogin-detail",
    ),
    path(
        "configuracao_core/imagemlogin/update/<uuid:pk>/",
        ImagemLoginUpdateView.as_view(),
        name="imagemlogin-update",
    ),
    path(
        "configuracao_core/imagemlogin/delete/<uuid:pk>/",
        ImagemLoginDeleteView.as_view(),
        name="imagemlogin-delete",
    ),
    path(
        "configuracao_core/imagemlogin/restore/<uuid:pk>/",
        ImagemLoginRestoreView.as_view(),
        name="imagemlogin-restore",
    ),
]


# URLs do Models LogoSistema
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/logosistema/",
        LogoSistemaListView.as_view(),
        name="logosistema-list",
    ),
    path(
        "configuracao_core/logosistema/create/",
        LogoSistemaCreateView.as_view(),
        name="logosistema-create",
    ),
    path(
        "configuracao_core/logosistema/<uuid:pk>/",
        LogoSistemaDetailView.as_view(),
        name="logosistema-detail",
    ),
    path(
        "configuracao_core/logosistema/update/<uuid:pk>/",
        LogoSistemaUpdateView.as_view(),
        name="logosistema-update",
    ),
    path(
        "configuracao_core/logosistema/delete/<uuid:pk>/",
        LogoSistemaDeleteView.as_view(),
        name="logosistema-delete",
    ),
    path(
        "configuracao_core/logosistema/restore/<uuid:pk>/",
        LogoSistemaRestoreView.as_view(),
        name="logosistema-restore",
    ),
]


# URLs do Models DadosGerais
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/dadosgerais/",
        DadosGeraisListView.as_view(),
        name="dadosgerais-list",
    ),
    path(
        "configuracao_core/dadosgerais/create/",
        DadosGeraisCreateView.as_view(),
        name="dadosgerais-create",
    ),
    path(
        "configuracao_core/dadosgerais/<uuid:pk>/",
        DadosGeraisDetailView.as_view(),
        name="dadosgerais-detail",
    ),
    path(
        "configuracao_core/dadosgerais/update/<uuid:pk>/",
        DadosGeraisUpdateView.as_view(),
        name="dadosgerais-update",
    ),
    path(
        "configuracao_core/dadosgerais/delete/<uuid:pk>/",
        DadosGeraisDeleteView.as_view(),
        name="dadosgerais-delete",
    ),
    path(
        "configuracao_core/dadosgerais/restore/<uuid:pk>/",
        DadosGeraisRestoreView.as_view(),
        name="dadosgerais-restore",
    ),
]


# URLs do Models RedeSocial
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/redesocial/",
        RedeSocialListView.as_view(),
        name="redesocial-list",
    ),
    path(
        "configuracao_core/redesocial/create/",
        RedeSocialCreateView.as_view(),
        name="redesocial-create",
    ),
    path(
        "configuracao_core/redesocial/<uuid:pk>/",
        RedeSocialDetailView.as_view(),
        name="redesocial-detail",
    ),
    path(
        "configuracao_core/redesocial/update/<uuid:pk>/",
        RedeSocialUpdateView.as_view(),
        name="redesocial-update",
    ),
    path(
        "configuracao_core/redesocial/delete/<uuid:pk>/",
        RedeSocialDeleteView.as_view(),
        name="redesocial-delete",
    ),
    path(
        "configuracao_core/redesocial/restore/<uuid:pk>/",
        RedeSocialRestoreView.as_view(),
        name="redesocial-restore",
    ),
]


# URLs do Models ImagemGenerica
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/imagemgenerica/",
        ImagemGenericaListView.as_view(),
        name="imagemgenerica-list",
    ),
    path(
        "configuracao_core/imagemgenerica/create/",
        ImagemGenericaCreateView.as_view(),
        name="imagemgenerica-create",
    ),
    path(
        "configuracao_core/imagemgenerica/<uuid:pk>/",
        ImagemGenericaDetailView.as_view(),
        name="imagemgenerica-detail",
    ),
    path(
        "configuracao_core/imagemgenerica/update/<uuid:pk>/",
        ImagemGenericaUpdateView.as_view(),
        name="imagemgenerica-update",
    ),
    path(
        "configuracao_core/imagemgenerica/delete/<uuid:pk>/",
        ImagemGenericaDeleteView.as_view(),
        name="imagemgenerica-delete",
    ),
    path(
        "configuracao_core/imagemgenerica/restore/<uuid:pk>/",
        ImagemGenericaRestoreView.as_view(),
        name="imagemgenerica-restore",
    ),
]


# URLs do Models ImagensSistema
urlpatterns += [
    path(
        "configuracao_core/",
        Configuracao_CoreIndexTemplateView.as_view(),
        name="configuracao_core-index",
    ),
    path(
        "configuracao_core/imagenssistema/",
        ImagensSistemaListView.as_view(),
        name="imagenssistema-list",
    ),
    path(
        "configuracao_core/imagenssistema/create/",
        ImagensSistemaCreateView.as_view(),
        name="imagenssistema-create",
    ),
    path(
        "configuracao_core/imagenssistema/<uuid:pk>/",
        ImagensSistemaDetailView.as_view(),
        name="imagenssistema-detail",
    ),
    path(
        "configuracao_core/imagenssistema/update/<uuid:pk>/",
        ImagensSistemaUpdateView.as_view(),
        name="imagenssistema-update",
    ),
    path(
        "configuracao_core/imagenssistema/delete/<uuid:pk>/",
        ImagensSistemaDeleteView.as_view(),
        name="imagenssistema-delete",
    ),
    path(
        "configuracao_core/imagenssistema/restore/<uuid:pk>/",
        ImagensSistemaRestoreView.as_view(),
        name="imagenssistema-restore",
    ),
]
