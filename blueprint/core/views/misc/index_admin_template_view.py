from base.settings import SYSTEM_NAME
from core.views.base import BaseTemplateView
from core.views.utils import get_breadcrumbs
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse


class IndexAdminTemplateView(
    LoginRequiredMixin, PermissionRequiredMixin, BaseTemplateView
):
    """Template View index"""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_ip"] = self.request.META.get(
            "HTTP_X_FORWARDED_FOR"
        ) or self.request.META.get("REMOTE_ADDR")
        url_str = "/"

        try:
            url_str = reverse("core:index")

        except Exception:
            url_str = "/core/"

        if "app_name" in context:
            url_str += context["app_name"]

        context["breadcrumbs"] = get_breadcrumbs(url_str)
        context["system_name"] = SYSTEM_NAME
        return context

    def has_permission(self):
        """
        Verifica se tem alguma das permissões retornadas pelo
        get_permission_required, caso tenha pelo menos uma ele
        retorna True
        """
        return (
            self.request.user is not None
            and self.request.user.is_authenticated
            and self.request.user.is_active
        )
