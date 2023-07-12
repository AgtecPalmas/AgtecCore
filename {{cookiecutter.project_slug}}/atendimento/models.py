import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import Base
from usuario.models import Usuario


class CriarAgendamentos(Base):
    """
    Cria agendamentos com base nas informações passadas dentro desta classe
    """

    evento = models.CharField(max_length=100, blank=True, null=True)
    data_inicial = models.DateField(
        "Data inicial",
        validators=[
            MinValueValidator(dt.date.today),
            MaxValueValidator(dt.date.today() + dt.timedelta(days=365)),
        ],
    )
    hora_inicial = models.TimeField("Hora inicial")
    data_final = models.DateField(
        "Data final",
        validators=[
            MinValueValidator(dt.date.today),
            MaxValueValidator(dt.date.today() + dt.timedelta(days=365)),
        ],
    )
    hora_final = models.TimeField("Hora final")
    numero_atendentes = models.PositiveIntegerField(
        "Número de Atendentes Simultâneos",
        validators=[MaxValueValidator(20), MinValueValidator(1)],
    )
    tempo_atendimento = models.PositiveIntegerField(
        "Tempo de Atendimento em MINUTOS",
        validators=[MaxValueValidator(360), MinValueValidator(1)],
    )
    atende_feriado = models.BooleanField(
        default=False, verbose_name="Atende feriado Nacional"
    )
    atende_24_horas = models.BooleanField(default=False, verbose_name="Atende 24 horas")
    atende_final_semana = models.BooleanField(
        default=False, verbose_name="Atende final de semana"
    )

    class Meta:
        verbose_name = "Criar Agendamentos"
        verbose_name_plural = "Criar Agendamentos"
        ordering = ["-data_inicial"]
        fields_display = [
            "evento",
            "data_inicial",
            "data_final",
            "hora_inicial",
            "hora_final",
            "numero_atendentes",
            "tempo_atendimento",
        ]

    def __str__(self):
        return "Criar Agendamentos"


class Atendente(Base):
    """
    Classe que representa um atendente
    """

    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = "Atendente"
        verbose_name_plural = "Atendentes"
        fields_display = ["nome"]
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class AtendimentoSituacao(models.IntegerChoices):
    """
    Situações do atendimento
    """

    LIVRE = 0
    AGENDADO = 1
    CANCELADO = 2
    CONFIRMADO = 3
    CONCLUIDO = 4
    NAO_CONFIRMADO = 5


class Atendimento(Base):
    """
    Classe que representa um atendimento\n
    Gerado automaticamente pela classe CriarAgendamentos\n
    ou manualmente
    """

    evento = models.CharField(max_length=100, blank=True, null=True)
    hora_inicial = models.TimeField("Hora de Início")
    hora_final = models.TimeField("Hora Final")
    data = models.DateField("Data")
    atendente = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        verbose_name="Atendente",
        blank=True,
        null=True,
        related_name="atendente",
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        verbose_name="Usuário",
        blank=True,
        null=True,
        related_name="usuario",
    )
    situacao = models.IntegerField(
        choices=AtendimentoSituacao.choices, default=AtendimentoSituacao.LIVRE
    )

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
        fields_display = [
            "evento",
            "hora_inicial",
            "hora_final",
            "data",
            "atendente",
            "usuario",
            "situacao",
        ]
        ordering = ["data", "hora_inicial", "hora_final"]

    def __str__(self):
        return f"{self.evento} - {self.data} - {self.hora_inicial} - {self.usuario}"
