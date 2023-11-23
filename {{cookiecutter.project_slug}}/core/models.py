import uuid

from base.settings import DELETED_MANY_TO_MANY, USE_DEFAULT_MANAGER
from core.middleware.current_user import get_current_user
from django.contrib.admin.utils import NestedObjects, quote
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRel,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import (
    AutoField,
    BooleanField,
    FileField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
    OneToOneField,
    OneToOneRel,
)
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

models.options.DEFAULT_NAMES += (
    "fk_fields_modal",
    "fields_display",
    "fk_inlines",
    "icon_model",
    "auditar",
)


class PaginacaoCustomizada(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100000


class BaseManager(models.Manager):
    def get_queryset(self):
        queryset = super(BaseManager, self).get_queryset()
        if (
            hasattr(self.model, "_meta")
            and hasattr(self.model._meta, "ordering")
            and self.model._meta.ordering
        ) or (
            (
                hasattr(self.model, "Meta")
                and hasattr(self.model.Meta, "ordering")
                and self.model.Meta.ordering
            )
        ):
            queryset = queryset.order_by(
                *(self.model._meta.ordering or self.model.Meta.ordering)
            )

        user = get_current_user()
        return (
            queryset.filter(deleted=False)
            if not user or not user.is_superuser
            else queryset
        )


class Base(models.Model):
    """Classe Base para ser herdada pelas demais
    para herdar os métodos e atributos
    objects_all [Manager auxiliar para retornar todos os registro
                 mesmo que o use_default_manager esteja como True]
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enabled = models.BooleanField("Ativo", default=True)
    deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(blank=True, null=True)

    # Verificação se deve ser usado o manager padrão ou o customizado
    if USE_DEFAULT_MANAGER is False:
        objects = BaseManager()
    else:
        objects = models.Manager()

    # Manager auxiliar para retornar todos os registro indepentende
    # da configuraçao do use_default_manager
    objects_all = models.Manager()

    def get_all_related_fields(self):
        """Método para retornar todos os campos que fazem referência ao
        registro que está sendo manipulado

        Returns:
            [Listas] -- [São retornadas duas listas a primeira com
                         os campos 'comuns' e a segunda lista os campos que
                         possuem relacionamento ManyToMany ou ForeignKey]
        """

        try:
            # Lista para retornar os campos que não são de relacionamento
            object_list = []

            # Lista para retornar os campos com relacionamento
            many_fields = []

            for field in self._meta.get_fields(include_parents=True):
                # Verificando se existe o atributo exclude no atributo que está sendo analisado
                if hasattr(self, "exclude") and (
                    field.name in Base().get_exclude_hidden_fields()
                    or field.name in self.exclude
                ):
                    continue

                # Desconsiderando o campo do tipo AutoField da análise
                if isinstance(field, AutoField):
                    continue

                # Desconsiderando os campos com atributos auto_now_add ou now_add da análise
                if hasattr(field, "auto_now_add") or hasattr(field, "now_add"):
                    continue

                # Verificando o tipo do relacionamento entre os campos
                if type(field) is ManyToManyField and DELETED_MANY_TO_MANY:
                    many_fields.append(
                        (
                            field.verbose_name or field.name,
                            self.__getattribute__(field.name).all() or None,
                        )
                    )

                elif type(field) is ManyToOneRel or type(field) is ManyToManyRel:
                    many_fields.append(
                        (
                            field.related_model._meta.verbose_name_plural or field.name,
                            self.__getattribute__(
                                field.related_name or f"{field.name}_set"
                            ),
                        )
                    )

                elif type(field) is GenericRel or type(field) is GenericForeignKey:
                    many_fields.append(
                        (
                            (
                                field.verbose_name
                                if hasattr(field, "verbose_name")
                                else None
                            )
                            or field.name,
                            self.object.__getattribute__(field.name),
                        )
                    )

                elif type(field) is OneToOneRel:
                    try:
                        object_list.append(
                            (
                                field.related_model._meta.verbose_name or field.name,
                                self.object.__getattribute__(field.name),
                            )
                        )
                    except Exception:
                        pass

                elif type(field) is BooleanField:
                    object_list.append(
                        (
                            (
                                field.verbose_name
                                if hasattr(field, "verbose_name")
                                else None
                            )
                            or field.name,
                            "Sim" if self.__getattribute__(field.name) else "Nâo",
                        )
                    )

                elif type(field) is ImageField or type(field) is FileField:
                    tag = ""
                    if self.__getattribute__(field.name).name:
                        if type(field) is ImageField:
                            tag = '<img width="100px" src="{url}" alt="{nome}" />'
                        elif type(field) is FileField:
                            tag = '<a  href="{url}" > <i class="fas fa-file"></i> {nome}</a>'
                        if tag:
                            tag = tag.format(
                                url=self.__getattribute__(field.name).url,
                                nome=self.__getattribute__(field.name).name.split(".")[
                                    0
                                ],
                            )

                    object_list.append(
                        (
                            (
                                field.verbose_name
                                if hasattr(field, "verbose_name")
                                else None
                            )
                            or field.name,
                            tag,
                        )
                    )

                else:
                    object_list.append(
                        (
                            (
                                field.verbose_name
                                if hasattr(field, "verbose_name")
                                else None
                            )
                            or field.name,
                            self.__getattribute__(field.name),
                        )
                    )

        finally:
            # Retornando as listas
            return object_list, many_fields

    def delete(self, using="soft_delete", keep_parents=False):
        """
        Sobrescrevendo o método para marcar os campos
        deleted como True e enabled como False. Assim o
        item não é excluído do banco de dados.
        """
        # Verificando se deve ser utilizado o manager costumizado
        if using == "default" or USE_DEFAULT_MANAGER is True:
            super(Base, self).delete()

        else:
            # Iniciando uma transação para garantir a integridade dos dados
            with transaction.atomic():
                # Recuperando as listas com os campos do objeto
                object_list, many_fields = self.get_all_related_fields()

                datetime_delete = timezone.now()

                # Percorrendo todos os campos que possuem relacionamento com o objeto
                for obj, values in many_fields:
                    if values is not None and values.all():
                        values.all().update(deleted=True, enabled=False, deleted_on=datetime_delete)

                # Atualizando o registro
                self.deleted = True
                self.enabled = False
                self.deleted_on = datetime_delete
                self.save(update_fields=["deleted", "enabled", "deleted_on"])

    class Meta:
        """Configure abstract class"""

        abstract = True
        ordering = ["id"]

    def get_exclude_hidden_fields(self):
        return ["enabled", "deleted", "deleted_on"]

    def get_meta(self):
        return self._meta

    def has_add_permission(self, request):
        opts = self._meta
        codename = get_permission_codename("add", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_change_permission(self, request, obj=None):
        opts = self._meta
        codename = get_permission_codename("change", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_delete_permission(self, request, obj=None):
        opts = self._meta
        codename = get_permission_codename("delete", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_view_permission(self, request, obj=None):
        opts = self._meta
        codename = get_permission_codename("view", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def __str__(self):
        return self.updated_on.strftime("%d/%m/%Y %H:%M:%S")


"""
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
                    Área dos models de Auditoria
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
=========================================================================
"""


class ParameterForBase(Base):
    nomeProjeto = models.TextField(blank=True, null=True, default="")
    tituloProjeto = models.TextField(blank=True, null=True, default="")
    descricaoProjeto = models.TextField(blank=True, null=True, default="")
    iconeProjeto = models.TextField(blank=True, null=True, default="")
    login_redirect_url = models.CharField(
        max_length=250, blank=True, null=True, default="/core/"
    )
    login_url = models.CharField(
        max_length=250, blank=True, null=True, default="/core/login/"
    )
    logout_redirect_url = models.CharField(
        max_length=250, blank=True, null=True, default="/core/login/"
    )
    url_integracao = models.CharField(max_length=500, blank=True, null=True, default="")
    audit_enable = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if parametro := ParameterForBase.objects.first():
            self.id = parametro.id
            self.pk = parametro.pk
        super(ParameterForBase, self).save()

    class Meta:
        verbose_name = "Parametro para o Core"
        verbose_name_plural = "Parametros para o Core"

    def __str__(self):
        return f"{self.nomeProjeto or self.id}"


class BaseMetod(models.Model):
    if USE_DEFAULT_MANAGER is False:
        objects = BaseManager()
    else:
        objects = models.Manager()

    objects_all = models.Manager()

    def get_all_related_fields(self, view=None, include_many_to_many=True):
        try:
            # Lista para retornar os campos que não são de relacionamento
            object_list = []

            # Lista para retornar os campos com relacionamento
            many_fields = []

            for field in self._meta.get_fields(include_parents=True):
                # Verificando se existe o atributo exclude no atributo que está sendo analisado

                if view and hasattr(view, "exclude") and field.name in view.exclude:
                    continue

                if (
                    view
                    and hasattr(view, "form_class")
                    and hasattr(view.form_class._meta, "exclude")
                    and view.form_class._meta.exclude is not None
                    and field.name in view.form_class._meta.exclude
                ):
                    continue

                if field.name in self.get_exclude_hidden_fields():
                    continue

                if not (
                    hasattr(self._meta, "model_name")
                    and self._meta.model_name
                    and self._meta.model_name == "audit"
                ):
                    # Desconsiderando o campo do tipo AutoField da análise
                    if isinstance(field, AutoField):
                        continue

                    # Desconsiderando os campos com atributos auto_now_add ou now_add da análise
                    if (
                        hasattr(field, "auto_now_add")
                        and field.auto_now_add is True
                        or hasattr(field, "auto_now")
                        and field.auto_now is True
                    ):
                        continue

                try:
                    # Verificando o tipo do relacionamento entre os campos
                    if type(field) is ManyToManyField and include_many_to_many:
                        if self.__getattribute__(field.name).exists():
                            many_fields.append(
                                (
                                    field.verbose_name or field.name,
                                    self.__getattribute__(field.name).all(),
                                    field.name,
                                )
                            )

                    elif (
                        (type(field) is ManyToOneRel or type(field) is ManyToManyRel)
                        or type(field) is GenericRel
                        or type(field) is GenericForeignKey
                    ):
                        if self.__getattribute__(
                            field.related_name or f"{field.name}_set"
                        ).exists():
                            many_fields.append(
                                (
                                    field.related_model._meta.verbose_name_plural
                                    or field.name,
                                    self.__getattribute__(
                                        field.related_name or f"{field.name}_set"
                                    ),
                                    field.related_name or f"{field.name}_set",
                                )
                            )

                    elif type(field) is GenericRelation:
                        if self.__getattribute__(field.name).exists():
                            many_fields.append(
                                (
                                    field.related_model._meta.verbose_name_plural
                                    or field.name,
                                    self.__getattribute__(field.name).all(),
                                    field.name,
                                )
                            )

                    elif (
                        type(field) is OneToOneRel
                        or type(field) is OneToOneField
                        or type(field) is ForeignKey
                    ):
                        object_list.append(
                            (
                                field.related_model._meta.verbose_name or field.name,
                                self.__getattribute__(field.name),
                                field.name,
                            )
                        )

                    elif type(field) is BooleanField:
                        object_list.append(
                            (
                                (
                                    field.verbose_name
                                    if hasattr(field, "verbose_name")
                                    else None
                                )
                                or field.name,
                                "Sim" if self.__getattribute__(field.name) else "Nâo",
                                field.name,
                            )
                        )

                    elif type(field) is ImageField or type(field) is FileField:
                        tag = ""
                        if self.__getattribute__(field.name).name:
                            if type(field) is ImageField:
                                tag = '<img width="100px" src="{url}" alt="{nome}" />'
                            elif type(field) is FileField:
                                tag = '<a  href="{url}" > <i class="fas fa-file"></i> {nome}</a>'
                            if tag:
                                tag = tag.format(
                                    url=self.__getattribute__(field.name).url,
                                    nome=self.__getattribute__(field.name).name.split(
                                        "."
                                    )[0],
                                )

                        object_list.append(
                            (
                                (
                                    field.verbose_name
                                    if hasattr(field, "verbose_name")
                                    else None
                                )
                                or field.name,
                                tag,
                                field.name,
                            )
                        )

                    elif hasattr(field, "choices") and hasattr(
                        self, f"get_{field.name}_display"
                    ):
                        object_list.append(
                            (
                                (
                                    field.verbose_name
                                    if hasattr(field, "verbose_name")
                                    else None
                                )
                                or field.name,
                                getattr(self, f"get_{field.name}_display")(),
                                field.name,
                            )
                        )

                    else:
                        object_list.append(
                            (
                                (
                                    field.verbose_name
                                    if hasattr(field, "verbose_name")
                                    else None
                                )
                                or field.name,
                                self.__getattribute__(field.name),
                                field.name,
                            )
                        )

                except Exception:
                    pass

        finally:
            # Retornando as listas
            return object_list, many_fields

    def get_deleted_objects(self, objs, user, using="default"):
        try:
            from django.db import models, router

            try:
                obj = objs[0]
            except IndexError:
                return [], {}, set(), []
            else:
                using = router.db_for_write(obj._meta.model)

        except Exception:
            using = "default"

        collector = NestedObjects(using=using)
        collector.collect(objs)
        perms_needed = set()

        def format_callback(obj):
            opts = obj._meta
            model = obj.__class__
            no_edit_link = f"{str(opts.verbose_name).title()}: {obj}"

            p = f'{opts.app_label}.{get_permission_codename("delete", opts)}'
            if not user.has_perm(p):
                perms_needed.add(opts.verbose_name.title())

            try:
                url = reverse(
                    f"{opts.app_label}:{opts.model_name}-update",
                    None,
                    (quote(obj.pk),),
                )

            except NoReverseMatch:
                # Change url doesn't exist -- don't display link to edit
                return no_edit_link

            # Display a link to the admin page.
            return format_html(
                '{}: <a href="{}">{}</a>', str(opts.verbose_name).title(), url, obj
            )

        to_delete = collector.nested(format_callback)

        protected = [format_callback(obj) for obj in collector.protected]
        model_count = {
            model._meta.verbose_name_plural: len(objs)
            for model, objs in collector.model_objs.items()
        }

        return perms_needed, protected

    def delete(self, using="soft_delete", keep_parents=False):
        if using == "default" or USE_DEFAULT_MANAGER is True:
            super().delete()

        else:
            # Iniciando uma transação para garantir a integridade dos dados
            with transaction.atomic():
                # Recuperando as listas com os campos do objeto
                object_list, many_fields = self.get_all_related_fields(
                    include_many_to_many=DELETED_MANY_TO_MANY
                )

                # Percorrendo todos os campos que possuem relacionamento com o objeto
                for itens in many_fields:
                    verbose_name, obj, fild_name = itens
                    if obj.all():
                        obj.all().update(deleted=True, enabled=False)

                # Atualizando o registro
                self.deleted = True
                self.enabled = False
                self.save(update_fields=["deleted", "enabled"])

    class Meta:
        """Configure abstract class"""

        abstract = True
        ordering = ["pk"]

    def get_exclude_hidden_fields(self):
        return [
            "deleted",
        ]

    def get_meta(self):
        return self._meta

    def has_add_permission(self, request):
        """
        Returns True if the given request has permission to add an object.
        Can be overridden by the user in subclasses.
        """
        opts = self._meta
        codename = get_permission_codename("add", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_change_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to change the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to change *any* object of the given type.
        """
        opts = self._meta
        codename = get_permission_codename("change", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_delete_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to delete the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to delete *any* object of the given type.
        """
        opts = self._meta
        codename = get_permission_codename("delete", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_view_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to change the given
        Django model instance, the default implementation doesn't examine the
        `obj` parameter.

        Can be overridden by the user in subclasses. In such case it should
        return True if the given request has permission to delete the `obj`
        model instance. If `obj` is None, this should return True if the given
        request has permission to delete *any* object of the given type.
        """
        opts = self._meta
        codename = get_permission_codename("view", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")


class Audit(BaseMetod):
    """
    Esse model faz a auditoria de alterações feitas nos models

    """

    num_revision = models.IntegerField(default=0, verbose_name="Audit Revision")
    data_type = models.ForeignKey(
        ContentType, verbose_name="Model", on_delete=models.PROTECT, null=True
    )
    tipo_revision = models.CharField(blank=True, null=True, max_length=255)
    fields_change = models.JSONField(
        blank=True,
        null=True,
        help_text=_("Form_principal or Model fields that have been modified"),
    )
    ip = models.CharField("IP do Responsável", max_length=50)
    previous_data_change = models.JSONField(
        help_text=_("before the time of the change")
    )
    current_data = models.JSONField(help_text=_("data at the time of the change"))
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("date created"),
        help_text="The date and time this revision was created.",
    )
    user_change = models.JSONField(
        verbose_name=_("user"), help_text=_("user who changed the data")
    )
    user_permissions_change = models.JSONField(
        verbose_name=_("user permissions"),
        help_text=_("permissions at the time of change"),
    )
    user_groups_change = models.JSONField(
        verbose_name=_("user groups"), help_text=_("groups at the time of change")
    )
    deleted = models.BooleanField(default=False, verbose_name="deleted")

    def __str__(self):
        return f"{self.created} - {self.user_change.get('fields').get('username')}"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    class Meta:
        ordering = ["data_type", "-created"]
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"
        icon_model = "fa fa-history"
