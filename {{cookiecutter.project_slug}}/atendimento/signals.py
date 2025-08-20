import datetime as dt

from django.db.models.signals import post_save
from django.dispatch import receiver

from atendimento.models import Atendente, Atendimento, CriarAgendamentos
from atendimento.utils import (
    data_is_feriado,
    data_is_weekday,
    horario_comercial,
    horario_sem_atendimento_minuto_zero,
)


@receiver(post_save, sender=CriarAgendamentos)
def __create_atendimentos(sender, **kwargs):
    """
    Cria atendimentos a partir de um agendamento\n
    Recebe um signal sempre que criado um agendamento
    """

    def __atendente_is_ocupado(
        self, atendente: Atendente, data: dt.date, hora: dt.time
    ) -> bool:
        return (
            Atendimento.objects.filter(
                atendente=atendente,
                data=data,
                hora_inicial__lte=hora,
                hora_final__gte=hora,
            ).count()
            >= 1
        )

    dados: object = kwargs["instance"]

    # Verifica se objeto é novo
    if dados.updated_at == dados.created_at and dados.deleted is False:
        data_in_while: dt.date = dados.data_inicial
        hora_in_while: dt.time = dados.hora_inicial
        # Loop nas datas
        while data_in_while <= dados.data_final:
            # Checa feriado ou se trabalha em feriado
            if not data_is_feriado(data_in_while) or dados.atende_feriado:
                # Checa se é dia útil ou se trabalha fim de semana
                if data_is_weekday(data_in_while) or dados.atende_final_semana:
                    # Checa horário atual está dentro do intervalo
                    while hora_in_while < dados.hora_final:
                        inicio_proximo_horario: dt.time = (
                            dt.datetime.combine(dt.date(1, 1, 1), hora_in_while)
                            + dt.timedelta(minutes=dados.tempo_atendimento)
                        ).time()
                        # Checa intervalo de trabalho
                        if (
                            horario_comercial(hora_in_while)
                            # Proximo horário dentro do intervalo
                            and inicio_proximo_horario
                            <= dados.hora_final  # Proximo horário dentro do intervalo de trabalho
                            and (
                                horario_comercial(inicio_proximo_horario)
                                # Proximo horário fora do intervalo mas com minuto zero
                                or horario_sem_atendimento_minuto_zero(
                                    inicio_proximo_horario
                                )
                            )
                        ) or dados.atende_24_horas:
                            # Para cada atendente, gera um atendimento
                            count_atendendimentos: int = 0
                            while count_atendendimentos < dados.numero_atendentes:
                                Atendimento.objects.create(
                                    evento=dados.evento,
                                    data=data_in_while,
                                    hora_inicial=hora_in_while,
                                    hora_final=inicio_proximo_horario,
                                )
                                count_atendendimentos += 1
                            count_atendendimentos: int = 0
                        hora_in_while: dt.time = inicio_proximo_horario
            data_in_while += dt.timedelta(days=1)
            hora_in_while: dt.time = dados.hora_inicial
