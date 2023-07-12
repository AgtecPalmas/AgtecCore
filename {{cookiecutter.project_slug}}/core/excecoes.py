class ExcecaoRegistroExistente(Exception):
    pass


class CpfCnpjValidationError(Exception):
    pass


def data_error(campo, msg):
    """
    Metodo que retona o dict padrao de error para o validade_data
    campo: nome do campo com erro
    msg: Mensagem do error.

    return: Retorna  um dict
    """
    return {"error_message": {campo: [msg]}}
