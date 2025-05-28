import datetime
import logging
from datetime import datetime
from email._header_value_parser import ContentType
from functools import wraps

from core.models import Audit, ParameterForBase
from core.templatetags.agtec_core import convert_listobject_for_json, get_ip
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

# Get an instance of a logger
logger = logging.getLogger(__name__)

user_model = get_user_model()


def item_equals_item(item, item2):
    """
    Função faz comparação entre dois objetos json para saber se tem alguma diferença nos dados
    :param item:
    :param item2:
    :return: dict_fields_atualizado
    """
    fields_atualizado = dict(item).copy()
    if "fields" in fields_atualizado:
        fields_atualizado.pop("fields")
    fields_atualizado["fields_atualizado"] = []
    for attr in item:
        if attr not in item2:
            return fields_atualizado
        if type(item[attr]) == dict and type(item2[attr]) == dict:
            fields_atualizado["fields_atualizado"] += item_equals_item(
                item[attr], item2[attr]
            )["fields_atualizado"]
        elif item[attr] != item2[attr]:
            fields_atualizado["fields_atualizado"].append(attr)
    return fields_atualizado


def list_contain_item(list_itens, item):
    """
    Faz uma comparação se a lista tem o item e caso tenha retorna o campo com as possiveis mudança de algum valor
    :param list_itens:
    :param item:
    :return: tuple(item, dict_filds_atualizados)
    """

    for item2 in list_itens:
        if ("pk" in item and "pk" in item2 and item["pk"] == item2["pk"]) or (
            "id" in item and "id" in item2 and item["id"] == item2["id"]
        ):
            fields_atualizado = item_equals_item(item, item2)
            if len(fields_atualizado["fields_atualizado"]) > 0:
                return None, fields_atualizado
            else:
                return item2, fields_atualizado
    return None, {}


def list_not_intersect(lista_1, lista_2):
    """
    Retorna uma tupla das listas passadas na respectiva ordem, com objetos em que seus campos divergem em relação a outra lista
    Resumindo pega tudo que não for uma intersecção entre as listas.
    :param lista_1:
    :param lista_2:
    :return:
    """
    objetos_atualizado = []
    for item in list(lista_1).copy():
        item_retornado2 = None
        item_retornado2, fields_atualizado = list_contain_item(lista_2, item)
        if fields_atualizado and len(fields_atualizado["fields_atualizado"]) > 0:
            objetos_atualizado.append(fields_atualizado)
        if item_retornado2 is not None:
            lista_2.remove(item_retornado2)
            lista_1.remove(item)
    return lista_1, lista_2, objetos_atualizado


def call_relationships_change(dict_object_prev, dict_object_next):
    """
        Faz a comparação dos objetos relacionados que foram alterados e cria uma lista de
        objetos de auditoria de cada elemento
    :param dict_object_prev:
    :param dict_object_next:
    :return: list_audit_relationships
    """
    lista1 = {}
    lista2 = {}
    if dict_object_prev and "relationships" in dict_object_prev:
        lista1 = dict(dict_object_prev["relationships"]).copy()

    if dict_object_next and "relationships" in dict_object_next:
        lista2 = dict(dict_object_next["relationships"]).copy()

    list_audit_relationships = []
    objetos_atualizado = []

    try:
        if lista1:
            for key, value_prev in dict(lista1).copy().items():
                if key in dict(lista2):
                    value_next = dict(lista2)[key]
                    (
                        diff_value_prev,
                        diff_value_next,
                        objetos_atualizado,
                    ) = list_not_intersect(
                        list(value_prev).copy(), list(value_next).copy()
                    )

                    if diff_value_prev:  # em casos de alteração
                        for item_prev in list(diff_value_prev).copy():
                            for item_next in list(diff_value_next).copy():
                                if item_prev["pk"] == item_next["pk"]:
                                    (app_name, model) = item_next["model"].split(".")
                                    audit = Audit()
                                    audit.fields_change = {
                                        "fields_model": [],
                                        "fields_form": [],
                                    }
                                    audit.data_type = ContentType.objects.filter(
                                        app_label=app_name, model=model
                                    ).first()
                                    audit.tipo_revision = "Edit Por Relacionamento"

                                    for fields_atualizado in objetos_atualizado:
                                        if item_prev["pk"] == fields_atualizado["pk"]:
                                            audit.fields_change = {
                                                "fields_model": fields_atualizado[
                                                    "fields_atualizado"
                                                ]
                                            }
                                            objetos_atualizado.remove(fields_atualizado)

                                    audit.previous_data_change = item_prev
                                    audit.current_data = item_next
                                    diff_value_prev.remove(item_prev)
                                    diff_value_next.remove(item_next)
                                    list_audit_relationships.append(audit)

                    # Tratando a operação de exclusão.
                    if diff_value_prev:
                        for item_prev in list(diff_value_prev).copy():
                            audit = Audit()
                            audit.fields_change = {
                                "fields_model": [],
                                "fields_form": [],
                            }
                            audit.fields_change = {"fields_model": []}
                            (app_name, model) = item_prev["model"].split(".")
                            audit.data_type = ContentType.objects.filter(
                                app_label=app_name, model=model
                            ).first()

                            if (
                                "pk" in item_prev
                                and item_prev.get("pk")
                                and audit.data_type.model_class()
                                .objects.filter(pk=item_prev.get("pk"))
                                .exists()
                            ):
                                audit.tipo_revision = "Retirado do Relacionamento"
                                audit.current_data = item_prev

                            else:
                                audit.tipo_revision = "Delete Por Relacionamento"
                                audit.current_data = {}

                            audit.previous_data_change = item_prev
                            diff_value_prev.remove(item_prev)
                            list_audit_relationships.append(audit)

                    if diff_value_next:  # em casos de inclusão
                        for item_next in list(diff_value_next).copy():
                            audit = Audit()
                            audit.fields_change = {
                                "fields_model": [],
                                "fields_form": [],
                            }
                            (app_name, model) = item_next["model"].split(".")
                            audit.data_type = ContentType.objects.filter(
                                app_label=app_name, model=model
                            ).first()

                            if "fields" in dict_object_prev:
                                audit.tipo_revision = "Add Por Relacionamento"
                                audit.previous_data_change = {}

                            else:
                                # a principio são casos de inclusões por inlines
                                audit.tipo_revision = "Add Vinculo"
                                audit.previous_data_change = lista1[key]

                            audit.current_data = item_next
                            diff_value_next.remove(item_next)
                            list_audit_relationships.append(audit)

                    # caso não esteja em nenhum então retira da lista
                    if key in lista2:
                        lista2.pop(key)
                    if key in lista1:
                        lista1.pop(key)

                elif lista1:
                    for item_relation in lista1[key]:
                        (app_name, model) = item_relation["model"].split(".")
                        audit = Audit()
                        audit.fields_change = {
                            "fields_model": [],
                            "fields_form": [],
                        }
                        audit.data_type = ContentType.objects.filter(
                            app_label=app_name, model=model
                        ).first()
                        audit.tipo_revision = "Delete Por Relacionamento"
                        audit.previous_data_change = item_relation
                        audit.current_data = {}
                        list_audit_relationships.append(audit)

            return list_audit_relationships

        # pega os casos de criação de novos objetos pai(super)
        if lista2:
            for item_relation in lista2.items():
                for item in item_relation[1]:
                    (app_name, model) = item["model"].split(".")
                    audit = Audit()
                    audit.fields_change = {"fields_model": [], "fields_form": []}
                    audit.data_type = ContentType.objects.filter(
                        app_label=app_name, model=model
                    ).first()
                    audit.tipo_revision = "Add Por Relacionamento"
                    audit.previous_data_change = {}
                    audit.current_data = item
                    list_audit_relationships.append(audit)

        # pega os casos de criação de novos objetos pai(super), porem os objetos ja existiam
        if "fields" not in dict_object_prev and lista1:
            for item_relation in lista1.items():
                for item in item_relation[1]:
                    (app_name, model) = item["model"].split(".")
                    audit = Audit()
                    audit.fields_change = {"fields_model": [], "fields_form": []}
                    audit.data_type = ContentType.objects.filter(
                        app_label=app_name, model=model
                    ).first()
                    audit.tipo_revision = "Add Vinculo"
                    audit.previous_data_change = item
                    audit.current_data = item
                    list_audit_relationships.append(audit)

        return list_audit_relationships

    except Exception as e:
        pass

    return list_audit_relationships


def get_related(obj, include_empy=False, form=None):
    """
        Pega todos os relacionamentos do objeto
    :param obj:
    :param include_empy:
    :param form:
    :return: list_relacionamentos
    """

    from django.contrib.contenttypes.fields import (
        GenericForeignKey,
        GenericRel,
        GenericRelation,
    )
    from django.db.models import (
        ForeignKey,
        ManyToManyField,
        ManyToManyRel,
        ManyToOneRel,
        OneToOneField,
        OneToOneRel,
    )

    list_relations = []
    for field in obj._meta.get_fields(include_parents=True):
        value = None
        # Verificando o tipo do relacionamento entre os campos
        if type(field) is ManyToManyField:
            if (
                form
            ):  # se true ele considera que é um inline e que esta sendo criado um item novo
                value = field.related_model.objects.filter(
                    id__in=form.data.get(field.name)
                )
            else:  # senão verifica se é os casos de  many do tipo select que apenas relaciona a um item ja existente
                value = obj.__getattribute__(field.name)

            if value and value.exists() or include_empy:
                list_relations.append(
                    (field.verbose_name or field.name, value.all(), field.name)
                )
        elif ((type(field) is ManyToOneRel or type(field) is ManyToManyRel)) or type(
            field
        ) is GenericRel:
            # se true ele considera que é um inline e que esta sendo criado um item novo
            if form:
                field_name = field.related_name or field.name

                # verifica se tem objeto criado e que está no forms
                if field_name in form.data:
                    # value = obj._meta.fields_map.get(field_name).related_model.objects.filter(id__in = form.data.get(field_name)).first()
                    value = field.related_model.objects.filter(
                        id__in=form.data.get(field_name)
                    ).first()

                # senão devolve uma consulta vasia
                else:
                    # value = obj._meta.fields_map.get(field_name).related_model.objects.none()
                    value = field.related_model.objects.none()

            # senão verifica se é os casos de  many do tipo select que apenas relaciona a um item ja existente
            else:
                value = obj.__getattribute__(field.related_name or f"{field.name}_set")

            if value and value.exists() or include_empy:
                list_relations.append(
                    (
                        field.related_model._meta.verbose_name_plural or field.name,
                        value,
                        field.related_name or f"{field.name}_set",
                    )
                )
        elif (
            value
            and type(field) is OneToOneRel
            or type(field) is OneToOneField
            or type(field) is ForeignKey
        ):
            # essa condição não usa o for pois o campo ele está diretamente ligado ao objeto
            value = (
                obj.__getattribute__(field.name) if hasattr(obj, field.name) else None
            )
            if value and type(value) is not ContentType:
                list_relations.append(
                    (
                        field.related_model._meta.verbose_name or field.name,
                        value,
                        field.name,
                    )
                )
        elif type(field) is GenericRelation:
            # essa condição não usa o for pois o campo ele está diretamente ligado ao objeto
            if hasattr(obj, field.name):
                value = obj.__getattribute__(field.name).all()
            else:
                value = None
            if value and value.exists() or include_empy:
                list_relations.append(
                    (
                        field.related_model._meta.verbose_name_plural or field.name,
                        value,
                        field.name,
                    )
                )
        elif type(field) is GenericForeignKey:
            value = (
                obj.__getattribute__(field.name) if hasattr(obj, field.name) else None
            )
            if value or include_empy:
                list_relations.append((field.name, value, field.name))
    return list_relations


def audit_delete(delete):
    """
    Responsavel por fazer auditoria quando algum objeto é excluido
    :param delete:
    :return:
    """

    @wraps(delete)
    def funcao_decorada(*args, **kwargs):
        result = None
        try:
            param = ParameterForBase.objects.first()
            view = args[0]
            form = args[1]
            cls = view.model

            # Checa audit Model
            model_audit = getattr(cls._meta, "auditar", settings.AUDIT_ENABLED)

            # Model sobrepõe Global
            if not model_audit or (not settings.AUDIT_ENABLED and not model_audit):
                return delete(*args, **kwargs)

            user_model = get_user_model()
            objetos_atualizado = []
            content_type_instance = ContentType.objects.get_for_model(cls)
            num_revision = (
                len(Audit.objects.filter(data_type=content_type_instance)) + 1
            )

            previous_instance = cls.objects.filter(id=kwargs.get("pk")).first()

            audit = Audit()
            audit.fields_change = {"fields_model": [], "fields_form": []}
            audit.created = datetime.now()

            if hasattr(view, "request") and view.request:
                request = view.request
                audit.ip = get_ip({"request": request})
                if request.user:
                    user = request.user

            if not user and hasattr(form, "user") and form.user:
                user = form.user

            if user:
                audit.user_change = convert_listobject_for_json(
                    [user_model.objects.filter(id=user.id).first()]
                )[0]
                audit.user_permissions_change = convert_listobject_for_json(
                    list(user.user_permissions.all())
                )
                audit.user_groups_change = convert_listobject_for_json(
                    list(user.groups.all())
                )
                for user_group in audit.user_groups_change:
                    list_permissions = []
                    if (
                        "fields" in user_group
                        and user_group["fields"]
                        and "permissions" in user_group["fields"]
                    ):
                        list_permissions = user_group["fields"]["permissions"]
                        user_group["fields"][
                            "permissions"
                        ] = convert_listobject_for_json(
                            list(Permission.objects.filter(id__in=list_permissions))
                        )

            audit.data_type = content_type_instance

            if previous_instance:
                # converte objeto 'previous_instance' com seus "atributos e relacionamenot diretos" para dict
                previous_instance_json = convert_listobject_for_json(
                    [
                        previous_instance,
                    ]
                )
                # como ja se sabe que é apenas um objeto então retira ele da lista
                if len(previous_instance_json) > 0:
                    previous_instance_json = previous_instance_json[0]

                # pega os "relacionamenot indiretos" do objeto 'previous_instance' e adciona ao dict do Objeto "previous_instance_json['relationships']"
                previous_instance_json["relationships"] = {}
                # ------ inicio bloco many nesse bloco ele busca os campos manyToMany e ao inves de colocar apenas a lista de id ele coloca a lista de objeto serealizado
                # Recuperando as listas com os campos do objeto
                many_fields_list = get_related(previous_instance, include_empy=True)
                for many_field in many_fields_list:
                    #  O if abaixo pega os relationships do tipo GenericRelatedObjectMananger ou qualquer tipo
                    #  que venha no metodo 'get_related' e que não tenha em _meta.fields_map
                    if (
                        "relationships" in previous_instance_json
                        and many_field[2] not in previous_instance_json["relationships"]
                    ):
                        if many_field[1]:
                            if hasattr(many_field[1], "all"):
                                previous_instance_json["relationships"][
                                    many_field[2]
                                ] = convert_listobject_for_json(many_field[1].all())
                            else:
                                previous_instance_json["relationships"][
                                    many_field[2]
                                ] = convert_listobject_for_json([many_field[1]])
                        else:
                            previous_instance_json["relationships"][many_field[2]] = {}
                    # retira os campos do fields pois ja tem em relationships
                    if (
                        "fields" in previous_instance_json
                        and len(many_field) > 0
                        and many_field[2] in previous_instance_json["fields"]
                    ):
                        previous_instance_json["fields"].pop(many_field[2])

                # ------ fim do bloco many
                audit.previous_data_change = previous_instance_json
            else:
                audit.previous_data_change = {}

            # aqui é pra fazer a comparação dos objetos relacionados que foram alterados e então chamar um signals para alterar ele tambem
            list_audit_relationships = call_relationships_change(
                audit.previous_data_change, audit.current_data
            )

            audit.current_data = {}

            audit.tipo_revision = "Delete"
            audit.num_revision = num_revision

            # ----------------------------------
            result = delete(*args, **kwargs)
            # ----------------------------------
        except Exception as e:
            logger.error(str(e))
            return result or delete(*args, **kwargs)
        try:
            audit.save()
            point_transaction = transaction.savepoint()
            if not cls.objects.filter(id=kwargs.get("pk")).exists():
                for audit_relationship in list_audit_relationships:
                    audit_relationship.created = datetime.now()
                    audit_relationship.num_revision = (
                        len(
                            Audit.objects.filter(data_type=audit_relationship.data_type)
                        )
                        + 1
                    )

                    if (
                        "pk" in audit_relationship.previous_data_change
                        and audit_relationship.previous_data_change.get("pk")
                        and audit_relationship.data_type.model_class()
                        .objects.filter(
                            pk=audit_relationship.previous_data_change.get("pk")
                        )
                        .exists()
                    ):
                        audit_relationship.tipo_revision = (
                            audit_relationship.tipo_revision.replace(
                                "Delete Por", "Retirado do"
                            )
                        )
                    id_model_pai = ""
                    if "pk" in audit.current_data and audit.current_data.get("pk"):
                        id_model_pai = audit.current_data.get("pk")
                    elif (
                        "pk" in audit.previous_data_change
                        and audit.previous_data_change.get("pk")
                    ):
                        id_model_pai = audit.previous_data_change.get("pk")
                    if id_model_pai:
                        audit_relationship.tipo_revision = f"{audit_relationship.tipo_revision} com '{content_type_instance.app_label}.{content_type_instance.model}(pk={id_model_pai})'"
                    audit_relationship.ip = audit.ip
                    audit_relationship.user_change = audit.user_change
                    audit_relationship.user_permissions_change = (
                        audit.user_permissions_change
                    )
                    audit_relationship.user_groups_change = audit.user_groups_change
                    audit_relationship.save()
            transaction.savepoint_commit(point_transaction)
            return result
        except Exception as erro:
            logger.error(str(erro))
            transaction.savepoint_rollback(point_transaction)
            return result or delete(*args, **kwargs)

    return funcao_decorada


def audit_save(save):
    """
    Responsavel por fazer a auditoria de objetos que tenha sido criados ou alterados
    :param save:
    :return:
    """

    @transaction.atomic()
    @wraps(save)
    def funcao_decorada(*args, **kwargs):
        result = None
        try:
            form = args[1]

            # Checa audit Model
            model_audit = getattr(
                form.instance._meta, "auditar", settings.AUDIT_ENABLED
            )

            # Model sobrepõe Global
            if not model_audit or (not settings.AUDIT_ENABLED and not model_audit):
                return save(*args, **kwargs)

            cls = form.instance.__class__
            request = None
            user = None
            user_model = get_user_model()
            objetos_atualizado = []

            fields_change = {"fields_model": [], "fields_form": []}

            content_type_instance = ContentType.objects.get_for_model(cls)
            num_revision = (
                len(Audit.objects.filter(data_type=content_type_instance)) + 1
            )

            # Verifica se é Adição
            if form.instance and form.instance._state.adding:
                type_action = "Add"

            # Verifica se é Edição
            elif form.instance and not form.instance.deleted:
                type_action = "Edit"
                # abaixo verifica se o campo modificado pertence ao modeu ou é apenas um campo do form
                for fild in form.changed_data:
                    if not hasattr(form.instance, fild):
                        fields_change["fields_form"].append(
                            {"field_form": fild, "value_field": form[fild].data}
                        )

            # Verifica se é Restauração
            else:
                type_action = "Restore"

            previous_instance = cls.objects.filter(id=form.instance.id).first()

            audit = Audit()
            audit.created = datetime.now()

            if getattr(form, "request", None):
                request = form.request
                audit.ip = get_ip({"request": request})
                if request.user:
                    user = request.user

            if not user and getattr(form, "user", None):
                user = form.user

            elif not user and getattr(args[0], "request", None):
                user = args[0].request.user

            if user:
                audit.user_change = convert_listobject_for_json(
                    [user_model.objects.filter(id=user.id).first()]
                )[0]
                audit.user_permissions_change = convert_listobject_for_json(
                    list(user.user_permissions.all())
                )
                audit.user_groups_change = convert_listobject_for_json(
                    list(user.groups.all())
                )
                for user_group in audit.user_groups_change:
                    list_permissions = []
                    if (
                        "fields" in user_group
                        and user_group["fields"]
                        and "permissions" in user_group["fields"]
                    ):
                        list_permissions = user_group["fields"]["permissions"]
                        user_group["fields"][
                            "permissions"
                        ] = convert_listobject_for_json(
                            list(Permission.objects.filter(id__in=list_permissions))
                        )

            audit.data_type = content_type_instance

            previous_relationships = {}
            # Verificando se existem dados no previous_instance
            if previous_instance:
                # converte objeto 'previous_instance' com seus "atributos e relacionamenot diretos" para dict
                previous_instance_json = convert_listobject_for_json(
                    [
                        previous_instance,
                    ]
                )
                # como ja se sabe que é apenas um objeto então retira ele da lista
                if len(previous_instance_json) > 0:
                    previous_instance_json = previous_instance_json[0]

                # pega os "relacionamenot indiretos" do objeto 'instance' e
                # adciona ao dict do Objeto 'instance_json['relationships']'
                previous_instance_json["relationships"] = {}
                # ------ inicio bloco many nesse bloco ele busca os campos manyToMany e ao
                # inves de colocar apenas a lista de id ele coloca a lista de objeto serealizado
                # Recuperando as listas com os campos do objeto
                many_fields_list = get_related(previous_instance, include_empy=True)
                for many_field in many_fields_list:
                    #  O if abaixo pega os relationships do tipo GenericRelatedObjectMananger ou qualquer tipo
                    #  que venha no metodo 'get_related' e que não tenha em _meta.fields_map
                    if "relationships" in previous_instance_json and not (
                        many_field[2] in previous_instance_json["relationships"]
                    ):
                        if many_field[1]:
                            if hasattr(many_field[1], "all"):
                                previous_instance_json["relationships"][
                                    many_field[2]
                                ] = convert_listobject_for_json(many_field[1].all())
                            else:
                                previous_instance_json["relationships"][
                                    many_field[2]
                                ] = convert_listobject_for_json([many_field[1]])
                        else:
                            previous_instance_json["relationships"][many_field[2]] = {}
                    # retira os campos do fields pois ja tem em relationships
                    if (
                        "fields" in previous_instance_json
                        and len(many_field) > 0
                        and many_field[2] in previous_instance_json["fields"]
                    ):
                        previous_instance_json["fields"].pop(many_field[2])

                audit.previous_data_change = previous_instance_json

            else:
                audit.previous_data_change = {}
                # pega os "relacionamenot indiretos" do objeto 'previous_instance' e
                # adciona ao dict do Objeto "previous_instance_json['relationships']"

                many_fields_list = get_related(
                    form.instance, form=form, include_empy=True
                )
                for many_field in many_fields_list:
                    #  O if abaixo pega os relationships do tipo GenericRelatedObjectMananger ou qualquer tipo
                    #  que venha no metodo get_related e que não tenha em _meta.fields_map
                    if not many_field[2] in previous_relationships:
                        if many_field[1]:
                            if hasattr(many_field[1], "all"):
                                previous_relationships[
                                    many_field[2]
                                ] = convert_listobject_for_json(many_field[1].all())
                            else:
                                previous_relationships[
                                    many_field[2]
                                ] = convert_listobject_for_json([many_field[1]])
                        else:
                            previous_relationships[many_field[2]] = {}
                audit.previous_data_change["relationships"] = previous_relationships
            # ----------------------------------
            result = save(*args, **kwargs)
            # ----------------------------------
            if form.instance and form.instance.pk:
                instance = form.instance.__class__.objects.filter(
                    id=form.instance.pk
                ).first()

                # instance = form.instance
                if instance is not None:
                    instance_json = convert_listobject_for_json(
                        [
                            instance,
                        ]
                    )
                    if len(instance_json) > 0:
                        instance_json = instance_json[0]

                    # pega os "relacionamenot indiretos" do objeto 'instance' e
                    # adciona ao dict do Objeto 'instance_json['relationships']'
                    instance_json["relationships"] = {}
                    # ------ inicio bloco many nesse bloco ele busca os campos manyToMany e ao
                    # inves de colocar apenas a lista de id ele coloca a lista de objeto serealizado
                    # Recuperando as listas com os campos do objeto
                    many_fields_list = get_related(instance, include_empy=True)
                    for many_field in many_fields_list:
                        #  O if abaixo pega os relationships do tipo GenericRelatedObjectMananger ou qualquer tipo
                        #  que venha no metodo get_related e que não tenha em _meta.fields_map
                        if "relationships" in instance_json and not (
                            many_field[2] in instance_json["relationships"]
                        ):
                            if many_field[1]:
                                if hasattr(many_field[1], "all"):
                                    instance_json["relationships"][
                                        many_field[2]
                                    ] = convert_listobject_for_json(many_field[1].all())
                                else:
                                    instance_json["relationships"][
                                        many_field[2]
                                    ] = convert_listobject_for_json([many_field[1]])
                            else:
                                instance_json["relationships"][many_field[2]] = {}

                        # retira os campos do fields pois ja tem em relationships
                        if (
                            "fields" in instance_json
                            and len(many_field) > 0
                            and many_field[2] in instance_json["fields"]
                        ):
                            instance_json["fields"].pop(many_field[2])
                    # ------ fim do bloco many
                    audit.current_data = instance_json
                else:
                    audit.current_data = {}

                # aqui é pra fazer a comparação dos objetos relacionados que foram alterados e
                # então chamar um signals para alterar ele tambem
                list_audit_relationships = call_relationships_change(
                    audit.previous_data_change, audit.current_data
                )

                if not previous_instance:
                    audit.previous_data_change = {}
                else:
                    """
                    Nesse fluxo do tratamento da auditoria é tratado apenas o objeto principal,
                    para facilitar o tratamento é realizada uma cópia do objeto a ser auditado
                    para o obj1 e para o obj2 os novos valores vindos do forms para realizar a
                    comparação.
                    """
                    obj1 = dict(previous_instance_json).copy()
                    obj2 = dict(instance_json).copy()
                    obj1.pop("relationships")
                    obj2.pop("relationships")
                    fields_change["fields_model"] = item_equals_item(obj1, obj2)[
                        "fields_atualizado"
                    ]
                    audit.fields_change = fields_change

                audit.tipo_revision = type_action
                audit.num_revision = num_revision
        except Exception as e:
            logger.error(str(e))
            if result:
                return result
            else:
                return save(*args, **kwargs)

        try:
            point_transaction = transaction.savepoint()
            for audit_relationship in list(list_audit_relationships).copy():
                fields_model = audit_relationship.fields_change["fields_model"]
                if (
                    audit_relationship.tipo_revision == "Edit Por Relacionamento"
                    and len(fields_model) <= 1
                    and "updated_at" in fields_model
                ):
                    list_audit_relationships.remove(audit_relationship)
                else:
                    data = None
                    if audit_relationship.current_data:
                        data = audit_relationship.current_data
                    elif audit_relationship.previous_data_change:
                        data = audit_relationship.previous_data_change
                    if data:
                        audit.fields_change["fields_model"].append(
                            {
                                "model": data["model"],
                                "pk": data["pk"],
                                "fields_change": fields_model,
                            }
                        )

            # trata o caso de ter apenas o update_on no pai
            __audit_updated_at = False
            __audit_fields_change_len = 0
            __audit_fields_model_exists = False
            __audit_fields_forms_exists = False
            if audit.fields_change is not None:
                # Verificando se o audit.fields_change é diferente de None para poder recuperar os valores
                __audit_fields_change_len = len(audit.fields_change["fields_model"])
                __audit_updated_at = "updated_at" in audit.fields_change["fields_model"]
                __audit_fields_model_exists = "fields_model" in audit.fields_change
                __audit_fields_forms_exists = "fields_forms" in audit.fields_change

            if (
                __audit_fields_change_len <= 1
                and __audit_updated_at
                and len(list_audit_relationships) <= 0
            ):
                audit.fields_change["fields_model"] = []

            # Verificando se está sendo realizado o update de um objeto
            if (
                list_audit_relationships
                or __audit_fields_model_exists
                or __audit_fields_forms_exists
            ):
                with transaction.atomic():
                    audit.save()
                for audit_relationship in list_audit_relationships:
                    audit_relationship.created = audit.created
                    __num_version = (
                        len(
                            Audit.objects.filter(data_type=audit_relationship.data_type)
                        )
                        + 1
                    )
                    audit_relationship.num_revision = __num_version
                    audit_relationship.ip = audit.ip

                    id_model_pai = ""
                    if "pk" in audit.current_data and audit.current_data.get("pk"):
                        id_model_pai = audit.current_data.get("pk")
                    elif (
                        "pk" in audit.previous_data_change
                        and audit.previous_data_change.get("pk")
                    ):
                        id_model_pai = audit.previous_data_change.get("pk")
                    if id_model_pai:
                        audit_relationship.tipo_revision = "%s com '%s.%s(pk=%s)'" % (
                            audit_relationship.tipo_revision,
                            content_type_instance.app_label,
                            content_type_instance.model,
                            id_model_pai,
                        )
                    audit_relationship.user_change = audit.user_change
                    audit_relationship.user_permissions_change = (
                        audit.user_permissions_change
                    )
                    audit_relationship.user_groups_change = audit.user_groups_change
                    audit_relationship.save()
            elif audit.current_data is not None:
                with transaction.atomic():
                    audit.save()
                for audit_relationship in list_audit_relationships:
                    audit_relationship.created = audit.created
                    __num_version = (
                        len(
                            Audit.objects.filter(data_type=audit_relationship.data_type)
                        )
                        + 1
                    )
                    audit_relationship.num_revision = __num_version
                    audit_relationship.ip = audit.ip

                    id_model_pai = ""
                    if "pk" in audit.current_data and audit.current_data.get("pk"):
                        id_model_pai = audit.current_data.get("pk")
                    elif (
                        "pk" in audit.previous_data_change
                        and audit.previous_data_change.get("pk")
                    ):
                        id_model_pai = audit.previous_data_change.get("pk")
                    if id_model_pai:
                        audit_relationship.tipo_revision = "%s com '%s.%s(pk=%s)'" % (
                            audit_relationship.tipo_revision,
                            content_type_instance.app_label,
                            content_type_instance.model,
                            id_model_pai,
                        )
                    audit_relationship.user_change = audit.user_change
                    audit_relationship.user_permissions_change = (
                        audit.user_permissions_change
                    )
                    audit_relationship.user_groups_change = audit.user_groups_change
                    audit_relationship.save()
            transaction.savepoint_commit(point_transaction)
            return result

        except Exception as erro:
            logger.error(str(erro))
            transaction.savepoint_rollback(point_transaction)
            if result:
                return result
            return save(*args, **kwargs)

    return funcao_decorada
