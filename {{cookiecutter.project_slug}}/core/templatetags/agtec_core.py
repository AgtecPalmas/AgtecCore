import django
from django import template
from django.core import serializers
import json
from django.template.defaultfilters import stringfilter
from django.urls import reverse

register = template.Library()


if django.VERSION[0] < 2 or (django.VERSION[0] == 2 and django.VERSION[1] <= 0):
    # tratando mudança de versão django 2.0
    from django.contrib.admin.templatetags.admin_modify import (
        submit_row as original_submit_row,
    )

    @register.inclusion_tag("admin/auth/base_user/submit_line.html", takes_context=True)
    def submit_row_user_boilerplate(context):
        # função utilizada para add o contexto dos botões submit para tela do change do user do core, foi substituida a original para não impactar outras telas
        ctx = original_submit_row(context)
        return ctx

else:
    # tratando mudança de versão django 2.1
    from django.contrib.admin.templatetags.base import InclusionAdminNode
    from django.contrib.admin.templatetags.admin_modify import submit_row

    @register.tag(name="submit_row_user_boilerplate")
    def submit_row_tag_user_boilerplate(parser, token):
        """
        Tag sobrescrita do admin_modify import submit_row para criar botões especificos para o usuario no Core do Boilerplate.
        função utilizada para add o contexto dos botões submit para tela do change do user do core, foi substituida a original para não impactar outras telas

        :param parser:
        :param token:
        :return:
        """
        return InclusionAdminNode(
            parser, token, func=submit_row, template_name="base_user/submit_line.html"
        )


@register.simple_tag(takes_context=True)
def get_ip(context):
    """Template tag to get user IP"""
    request = context["request"]
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@register.filter(name="conv_list_for_json")
def convert_listobject_for_json(listobject):
    listobject_str_json = serializers.serialize("json", listobject)
    listobject_dict_json = json.loads(listobject_str_json)
    if len(listobject_dict_json) > 0:
        return listobject_dict_json
    else:
        return {}


# pegar um atributo de um dicionario
# motivo: No template não acessa var que começa com _
@register.filter(name="get")
def get(d, k):
    return d.get(k, None)


# Retorna os fields manytomany
@register.filter(name="get_many_to_many")
def get_many_to_many(obj, object_list):
    manytomany_name = []
    manytomany = []
    for field in obj._meta.many_to_many:
        manytomany_name.append(field._m2m_reverse_name_cache)

    for item in object_list:
        try:
            if item[1].target_field_name in manytomany_name:
                manytomany.append(item[1])
        except Exception:
            pass

    return manytomany


@register.filter(name="include_empty_form")
def include_empty_form(formset):
    """
    Certifique-se de que o "formulário vazio" esteja incluído ao exibir um formset (geralmente tabela com linhas de entrada)

    Essa templatetag é usada para acrescentar o enpy_form na lista de formset, para poder ter os campos bases que vão ser add.
    """
    for form in formset:
        yield form
    if hasattr(formset, "empty_form"):
        yield formset.empty_form


@register.filter()
def has_add_permission(model=None, request=None):
    """
    Verifica se o usuario tem a permissão de adicionar, no model passado

    ex: {if model|has_add_permission:request %}
    """
    if model and hasattr(model, "has_add_permission") and request:
        return model.has_add_permission(request=request)
    else:
        return False


@register.filter()
def has_change_permission(model=None, request=None):
    """
    Verifica se o usuario tem a permissão de alterar, no model passado

    ex: {if model|has_change_permission:request %}
    """
    if model and hasattr(model, "has_change_permission") and request:
        return model.has_change_permission(request=request)
    else:
        return False


@register.filter()
def has_delete_permission(model=None, request=None):
    """
    Verifica se o usuario tem a permissão de deletar, no model passado

    ex: {if model|has_delete_permission:request %}
    """
    if model and hasattr(model, "has_delete_permission") and request:
        return model.has_delete_permission(request=request)
    else:
        return False


@register.filter(name="has_perm")
def has_perm(user, permissao):
    return user.has_perm(permissao)


@register.filter(name="is_type")
def is_type(valor, tipo):
    return str(type(valor)).split("'")[1] == tipo


@register.filter
@stringfilter
def split(string, sep):
    """Return the string split by sep.

    Example usage: {{ value|split:"/" }}
    """
    return string.split(sep)


@register.filter
def in_list(value, the_list):
    """Return the True or False

    Example usage: {{ value|in:list }}
    """
    if the_list is None or len(the_list) <= 0:
        return False
    if isinstance(the_list, str):
        the_list = the_list.split(",")
    else:
        the_list = list(the_list)
    return value in the_list


@register.filter
def link_detail_model(value):
    """Capitalize the first character of the value."""
    url = ""
    tag_a = ""
    try:
        viewname = "%s:%s-detail" % (value._meta.app_label, value._meta.model_name)
        url = reverse(viewname, kwargs={"pk": value.pk})
        tag_a = url
    except:
        return None
    return tag_a


@register.filter
def contains_in_list(value, the_list):
    """Return the True or False caso contenha o elemnto na lista ou parte dele
    parecido com o in_list, porem ele pega elemnto por elemnto da lista e olha se a string contem o value

    Example usage: {{ value|in:list }}

    """
    if the_list is None or len(the_list) <= 0:
        return False
    if isinstance(the_list, str):
        the_list = the_list.split(",")
    else:
        the_list = list(the_list)

    for elemento in the_list:
        if value in elemento:
            return True
    return value in the_list


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        current = context
        # inverte a lista para acelerar o processo
        for dic_context in list(reversed(context.dicts)):
            if self.var_name in dic_context:
                current = dic_context
        current[self.var_name] = value
        return ""


@register.tag(name="set")
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError(
            "'set' tag must be of the form: {% set <var_name> = <var_value> %}"
        )

    return SetVarNode(parts[1], parts[3])
