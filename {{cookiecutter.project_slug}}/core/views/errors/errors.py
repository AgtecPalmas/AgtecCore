from core.views.base import BaseTemplateView


class BaseErrorView(BaseTemplateView):
    status_code: int = 500
    template_name: str = "errors/base.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = self.status_code or 500
        return response


class BadRequestView(BaseErrorView):
    template_name = "errors/bad_request.html"
    status_code = 400


class PageNotFoundView(BaseErrorView):
    template_name = "errors/page_not_found.html"
    status_code = 404


class PermissionDeniedView(BaseErrorView):
    template_name = "errors/permission_denied.html"
    status_code = 403


class ServerErrorView(BaseErrorView):
    template_name = "errors/server_error.html"
    status_code = 500
