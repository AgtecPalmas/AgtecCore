from django import template
from django.utils.safestring import mark_safe
from usuario.models import Usuario

register = template.Library()


@register.simple_tag(takes_context=True)
def set_attribute_display_username(context):
    """TemplateTag responsável por chamar a função Usuario.get_display_username()
    passando o user logado que retorna o atributo que será utilizado no template
    header_menu.html
    """
    try:
        request = context["request"]
        return Usuario.get_display_username(request.user)
    except Exception as error:
        return "AgtecCore"


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


@register.filter()
def has_add_permission(model=None, request=None):
    """
    Verifica se o usuário tem a permissão de adicionar, no model passado

    ex: {if model|has_add_permission:request %}
    """
    if model and hasattr(model, "has_add_permission") and request:
        return model.has_add_permission(request=request)
    else:
        return False


@register.filter()
def has_view_permission(model=None, request=None):
    """
    Verifica se o usuário tem a permissão de adicionar, no model passado
    ex: {if model|has_add_permission:request %}
    """
    __app, __model = model.get("path_url").split(":")
    __model = __model.split("-")[0]
    __permission = f"{__app}.view_{__model}"
    if model and request:
        return request.user.has_perm(__permission)
    else:
        return False


@register.filter()
def has_change_permission(model=None, request=None):
    """
    Verifica se o usuario tem a permissão de alterar, no model passado
    ex: {if model|has_change_permission:request %}
    """
    __app, __model = model.get("path_url").split(":")
    __model = __model.split("-")[0]
    __permission = f"{__app}.change_{__model}"
    if model and request:
        return request.user.has_perm(__permission)
    else:
        return False


@register.filter()
def has_delete_permission(model=None, request=None):
    """
    Verifica se o usuario tem a permissão de deletar, no model passado
    ex: {if model|has_delete_permission:request %}
    """
    __app, __model = model.get("path_url").split(":")
    __model = __model.split("-")[0]
    __permission = f"{__app}.delete_{__model}"
    if model and request:
        return request.user.has_perm(__permission)
    else:
        return False


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Atualizando as urls de paginação com filtros e buscas
    """

    query = context["request"].GET.copy()

    for kwarg in kwargs:
        try:
            query.pop(kwarg)
        except KeyError:
            pass

    # Atualizando o valor da página (inteiro) para uma String
    kwargs.update({"page": str(kwargs.get("page"))})

    query.update(kwargs)

    return mark_safe(query.urlencode())
