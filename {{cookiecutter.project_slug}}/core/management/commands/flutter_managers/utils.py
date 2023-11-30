from core.management.commands.constants.flutter import IGNORE_FIELDS


def ignore_base_fields(field) -> bool:
    """Método responsável por remover da análise do models os atributos herdados da classe pai Base

    Arguments:
        field {String} -- Nome do atributo

    Returns:
        bool -- True se o atributo for um dos atributos da classe pai, caso contrário False.
    """
    try:
        return field in IGNORE_FIELDS
    except Exception as error:
        raise error


def convert_to_camel_case(text: str) -> str:
    """
    Método para converter um texto para o padrão Camel
    Case no padrão do Flutter

    Parameters
    ----------
    text : str
        Texto a ser convertido

    Returns
    -------
    str
        Texto convertido

    Raises
    ------
    error
        Erro ao converter o texto
    """
    try:
        components = text.split("_")
        if len(components) == 1:
            __string = components[0]
            return f"{__string[:1].lower()}{__string[1:]}"
        return components[0] + "".join(x.title() for x in components[1:])
    except Exception as error:
        raise error
