from django.urls import path

from core.views.audit import (
    AuditDetailView,
    AuditListView,
    AuditObjectListView,
    AuditTemplateView,
)
from core.views.auth import (
    LoginView,
    LogoutView,
    RequestPassword,
    ResetPassword,
    UpdatePassword,
)
from core.views.misc import (
    IndexAdminTemplateView,
    ProfileUpdateView,
    ProfileView,
    SettingsView,
)

app_name = "core"
urlpatterns = [
    path("", IndexAdminTemplateView.as_view(), name="index"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/update/password/", UpdatePassword.as_view(), name="password-update"),
    path(
        "profile/request_password/", RequestPassword.as_view(), name="password-request"
    ),
    path(
        "profile/reset/password/<str:email_code>",
        ResetPassword.as_view(),
        name="password-reset",
    ),
    path("settings/", SettingsView.as_view(), name="settings"),
]

# Auditoria
urlpatterns += [
    path("audit/", AuditTemplateView.as_view(), name="audit-index"),
    path("audit/audit/", AuditListView.as_view(), name="audit-list"),
    path("audit/<int:pk>/", AuditDetailView.as_view(), name="audit-detail"),
    path(
        "<path:object_id>/<int:pk>/audit/",
        AuditListView.as_view(),
        name="audit-detail_model-list",
    ),
    path(
        "<path:object_id>/audit/",
        AuditObjectListView.as_view(),
        name="audit-list_model-list",
    ),
    path(
        "<path:object_id>/audit/<int:pk>/",
        AuditDetailView.as_view(),
        name="audit-list_model-detail",
    ),
    path(
        "<path:object_id>/<int:id>/audit/<int:pk>/",
        AuditDetailView.as_view(),
        name="audit-detail_model-detail",
    ),
]
