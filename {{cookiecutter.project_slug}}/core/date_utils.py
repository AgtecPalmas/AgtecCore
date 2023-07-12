from datetime import datetime

import dateparser


def get_datetime_obj(data_str, format, format_str):
    """
    Retorna um objeto DateTime de acordo com o formato especificado
    :param data_str: a string contendo a data
    :param format: o formato que o sistema deve utilizar para formatar, seguindo os padrões definidos na documentação do
                   método strptime. link: (https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)
    :param format_str: uma string representando o formato de data esperado. Ex. 'dd/mm/yyyy'
    :return:
    """
    try:
        return datetime.strptime(data_str, format)
    except ValueError as value_error:
        raise ValueError(f"Informe uma data no formato {format_str}") from value_error


def get_data(data_str):
    if not isinstance(data_str, str):
        return data_str
    return get_datetime_obj(
        data_str,
        "%d/%m/%Y" if "/" in data_str else "%d-%m-%Y",
        "dd/mm/yyyy" if "/" in data_str else "dd-mm-yyyy",
    )


def get_data_format_ddmmyyyy(data):
    return data.strftime("%d/%m/%Y")


def obtenha_data_i10n(data_i10n_str, formato=None):
    """
    :param data_i10n_str: data em string
    :param formato: exemplo, %d/%m/%Y
    :return: datetime
    """
    cfg = {}
    if formato:
        cfg.update(date_formats=formato)

    if isinstance(data_i10n_str, str):
        return dateparser.parse(data_i10n_str, **cfg)
    return data_i10n_str
