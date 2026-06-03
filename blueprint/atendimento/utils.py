import holidays
import datetime as dt
from decouple import config, Csv


def data_is_feriado(data: dt.date) -> bool:
    feriados = holidays.Brazil()
    return data in feriados


def data_is_weekday(data: dt.date) -> bool:
    return str(data.weekday()) in config('DIAS_DA_SEMANA', cast=Csv())


def horario_comercial(hora: dt.time) -> bool:
    return str(hora.hour) not in config('HORAS_SEM_ATENDIMENTO', cast=Csv())


def horario_sem_atendimento_minuto_zero(hora: dt.time) -> bool:
    return str(hora.hour) in config('HORAS_SEM_ATENDIMENTO', cast=Csv()) and hora.minute == 0
