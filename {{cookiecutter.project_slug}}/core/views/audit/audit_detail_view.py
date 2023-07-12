from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from core.forms import AuditForm
from core.models import Audit, ParameterForBase
from core.views.base import BaseDetailView
from core.views.utils import get_apps, get_breadcrumbs, get_default_context_data


class AuditDetailView(BaseDetailView):
    """View para gerenciar o detail do Audit"""

    model = Audit
    form_class = AuditForm
    context_object_name = "audit"
    template_name = "audit/audit_detail.html"
    extra_context = {"parameter": ParameterForBase.objects.first}

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data(**kwargs)
        object_list, many_fields = self.object.get_all_related_fields(view=self)
        context["object_list"] = object_list
        context["many_fields"] = many_fields
        context = get_default_context_data(context, self)

        model_class = None

        if self.kwargs and "object_id" in self.kwargs:
            itens_kwargs = self.kwargs.get("object_id", "/").split("/")
            contentType = None

            if len(itens_kwargs) == 1:
                name_app = itens_kwargs[0]

            elif len(itens_kwargs) >= 2:
                (name_app, name_model) = itens_kwargs[:2]
                contentType = ContentType.objects.filter(
                    app_label=name_app, model=name_model
                ).first()

            if contentType:
                model_class = contentType.model_class()

        if model_class:
            context["url_list"] = "{app}:{model}-list".format(
                app=model_class._meta.app_label, model=model_class._meta.model_name
            )

            context["model_name"] = (
                model_class._meta.verbose_name
                or model_class._meta.verbose_name_plural
                or model_class._meta.model_name
                or model_class._meta.object_name
            ).title()

            url_audit = reverse(context["url_list"])

            if "pk" in self.kwargs:
                context["url_audit"] = f'{url_audit}{self.kwargs.get("pk", "")}/audit/'

            else:
                context["url_audit"] = f"{url_audit}audit/"

        else:
            context["url_list"] = "{app}:{model}-list".format(
                app=self.model._meta.app_label, model=self.model._meta.model_name
            )

            context["model_name"] = (
                self.model._meta.model_name
                or self.model._meta.verbose_name_plural
                or self.model._meta.object_name
            ).title()

        context["object_pk"] = context["object"].current_data.get("pk")

        try:
            context["object"] = (
                ContentType.objects.get(app_label=name_app, model=name_model)
                .model_class()
                .objects.get(pk=context["object_pk"])
            )
        except Exception:
            pass

        if len(self.kwargs) == 1:
            url_str = f'{reverse(context["url_list"])}audit/'
        else:
            url_str = f'{reverse(context["url_list"])}{context["object_pk"]}/audit/ Detalhes {self.kwargs.get("pk", "")}'
        context["breadcrumbs"] = get_breadcrumbs(url_str)

        context["apps"] = get_apps()
        # context['notifications'] = get_notifications(self)

        context["has_add_permission"] = self.model().has_add_permission(self.request)
        context["has_change_permission"] = self.model().has_change_permission(
            self.request
        )
        context["has_delete_permission"] = self.model().has_delete_permission(
            self.request
        )
        context["has_view_permission"] = self.model().has_view_permission(self.request)

        context["has_audit_permission"] = self.request.user.has_perm("core.view_audit")

        return context
