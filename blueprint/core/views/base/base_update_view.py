from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from core.decorators import audit_save
from core.forms import BaseForm
from core.models import Base
from core.views.utils import get_breadcrumbs, get_default_context_data, get_url_str


class BaseUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    """
    Classe base que deve ser herdada caso o desenvolvedor queira reaproveitar
    as funcionalidades já desenvolvidas para UpdateView
    Na classe que herdar dessa deve ser atribuido o valor template_name com o caminho até o template HTML a ser renderizado

    Raises:
        ValidationError -- Caso não seja atribuido o valor da variavel template_name ocorrerá uma excessão
    """

    model = Base
    form_class = BaseForm
    template_name_suffix = "_update"
    inlines = []

    def __init__(self):
        super(BaseUpdateView, self).__init__()
        self.app_name = self.model._meta.app_label
        self.model_name = self.model._meta.model_name

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        return ["outside_template/base_update.html"]

    def get_success_url(self):
        if self.success_url and self.success_url != "":
            return self.success_url

        else:
            return reverse(
                f"{self.app_name}:{self.model_name}-detail",
                kwargs={"pk": self.object.pk},
            )

    def get_permission_required(self):
        """
        cria a lista de permissões que a view pode ter de acordo com cada model.
        """
        return (f"{self.app_name}.change_{self.model_name}",)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        for modal in getattr(self, "form_modals", []):
            context[f"form_{modal.Meta.model.__name__.lower()}"] = modal

        context["list_inlines"] = self.get_formset_inlines()
        context = get_default_context_data(context, self)

        url_str = get_url_str(context["url_list"], f"Atualizar {context['object'].pk}")
        context["breadcrumbs"] = get_breadcrumbs(url_str)
        return context

    def get_formset_inlines(self):
        """Metodo utilizado para instanciar os inlines.
        Returns:
            List -- Lista com os formulários inline do form principal
        """
        formset_inlines = []
        if hasattr(self, "inlines") and self.inlines:
            for item in self.inlines:
                if item.model().has_change_permission(self.request):
                    if self.request.POST:
                        formset = item(
                            self.request.POST,
                            self.request.FILES,
                            instance=self.object,
                            prefix=item.model._meta.model_name,
                        )

                    else:
                        formset = item(
                            instance=self.object, prefix=item.model._meta.model_name
                        )

                    lista_instance_inline = formset.queryset.all() or []

                    # só seta True caso os valores definidos na permissão do usuario e o can_delete do inlineformset_factory seja True
                    formset.can_delete = (
                        item.model().has_delete_permission(self.request)
                        and item.can_delete
                    )

                    # se não tem permisão de excluir, então seta o valor minimo para 0
                    if not formset.can_delete:
                        formset.min_num = 0

                    # se não tem permisão de adcionar, então seta o valor minimo para 0
                    if not item.model().has_add_permission(self.request):
                        formset.max_num = 0

                    # pode ser colocado o user aqui para utilizar na validação do forms
                    if hasattr(formset, "prefix") and formset.prefix:
                        formset.form.user = self.request.user
                        formset_inlines.append(formset)

        return formset_inlines

    def get_form_kwargs(self):
        """Método utilizado para adicionar o request

        Returns:
            Kwargs
        """
        kwargs = super(BaseUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    @audit_save
    def form_valid(self, form):
        """Método para verificar se o formulário submetido está válido

        Arguments:
            form {Form} -- Formulário com os valores enviado para processamento

        Returns:
            Url -- O retorno é o redirecionamento para a URL de sucesso configurada na Views da app
        """

        formset_inlines = self.get_formset_inlines()
        if form.is_valid():
            for form_formset in formset_inlines:
                if not form_formset.is_valid():
                    return self.render_to_response(
                        context=self.get_context_data(
                            form=form, named_formsets=formset_inlines
                        )
                    )

            self.object = form.save()

            # for every formset, attempt to find a specific formset save function
            # otherwise, just save.
            for formset in formset_inlines:
                formset.instance = self.object
                formset.save()

            messages.success(
                request=self.request,
                message=f"'{self.object}', Alterado com Sucesso!",
                extra_tags="success",
            )

        else:
            messages.error(
                request=self.request,
                message="Ocorreu um erro, verifique os campos!",
                extra_tags="danger",
            )
            return form.errors

        # salva e add outro novo_continue
        if "_addanother" in form.data:
            return redirect(reverse(self.get_context_data()["url_create"]))

        # salva e continua editando
        elif "_continue" in form.data:
            return redirect(
                reverse(
                    self.get_context_data()["url_update"], kwargs={"pk": self.object.pk}
                )
            )

        # salva e redireciona pra lista
        else:
            return redirect(self.get_success_url())
