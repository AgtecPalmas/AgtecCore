import json

from django import template
from django.core import serializers
from django.template.defaultfilters import stringfilter
from django.urls import reverse

register = template.Library()


@register.filter(name="conv_list_for_json")
def convert_listobject_for_json(listobject):
    listobject_str_json = serializers.serialize("json", listobject)
    listobject_dict_json = json.loads(listobject_str_json)
    return listobject_dict_json if len(listobject_dict_json) > 0 else {}


@register.filter(name="include_empty_form")
def include_empty_form(formset):
    """
    Certifique-se de que o "formulário vazio" esteja incluído ao exibir um formset (geralmente tabela com linhas de entrada)

    Essa templatetag é usada para acrescentar o enpy_form na lista de formset, para poder ter os campos bases que vão ser add.
    """
    yield from formset
    if hasattr(formset, "empty_form"):
        yield formset.empty_form


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
    the_list = the_list.split(",") if isinstance(the_list, str) else list(the_list)
    return value in the_list


@register.filter
def link_detail_model(value):
    """Capitalize the first character of the value."""
    url = ""
    tag_a = ""
    try:
        viewname = f"{value._meta.app_label}:{value._meta.model_name}-detail"
        url = reverse(viewname, kwargs={"pk": value.pk})
        tag_a = url
    except Exception:
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
    the_list = the_list.split(",") if isinstance(the_list, str) else list(the_list)
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
        for dic_context in list(reversed(current.dicts)):
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
