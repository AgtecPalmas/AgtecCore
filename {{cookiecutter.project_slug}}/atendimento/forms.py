from datetime import datetime
from core.forms import BaseForm
from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker
import datetime as dt
from .models import Atendente, Atendimento, CriarAgendamentos


class CriarAgendamentosForm(BaseForm):
    """Form padrão para o model CriarAgendamentos"""

    data_inicial = forms.DateField(
        widget=DatePicker(
            options={
                "minDate": datetime.now().strftime("%Y-%m-%d"),
            }
        )
    )

    data_final = forms.DateField(
        widget=DatePicker(
            options={
                "minDate": datetime.now().strftime("%Y-%m-%d"),
            }
        )
    )

    hora_inicial = forms.TimeField(
        widget=TimePicker(
            options={
                "stepping": 10,
                "format": "HH:mm",
            }
        )
    )

    hora_final = forms.TimeField(
        widget=TimePicker(
            options={
                "stepping": 10,
                "format": "HH:mm",
            }
        )
    )

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = CriarAgendamentos

    def clean(self):
        cleaned_data = super().clean()

        # Validações de Data
        if not cleaned_data.get("data_inicial") or not cleaned_data.get("data_final"):
            raise forms.ValidationError("Datas não podem ficar vazias.")

        elif cleaned_data["data_inicial"] > cleaned_data["data_final"]:
            self.add_error(
                "data_inicial", "Data inicial não pode ser maior que data final."
            )

        elif cleaned_data["data_final"] - cleaned_data["data_inicial"] > dt.timedelta(
            days=31
        ):
            self.add_error("data_final", "Período de atendimento maior que 31 dias")

        # Validações de Hora
        if not cleaned_data.get("hora_inicial") or not cleaned_data.get("hora_final"):
            raise forms.ValidationError("Horários não podem ficar vazios.")

        elif cleaned_data["hora_final"] < cleaned_data["hora_inicial"]:
            self.add_error(
                "hora_final", "Hora final não pode ser menor que hora inicial."
            )

        elif cleaned_data["hora_final"] == cleaned_data["hora_inicial"]:
            self.add_error("hora_final", "Horários não podem ser iguais.")

        elif not cleaned_data.get("tempo_atendimento"):
            self.add_error("tempo_atendimento", "Indique a duração do atendimento.")

        elif dt.datetime.combine(
            dt.date(1, 1, 1), cleaned_data["hora_final"]
        ) - dt.datetime.combine(
            dt.date(1, 1, 1), cleaned_data["hora_inicial"]
        ) < dt.timedelta(
            minutes=cleaned_data["tempo_atendimento"]
        ):
            self.add_error(
                "tempo_atendimento",
                "Período de tempo não pode ser menor que o tempo de atendimento",
            )

    def save(self):
        # Adiciona o dia do agendamento caso não haja título
        if not self.cleaned_data["evento"]:
            self.cleaned_data[
                "evento"
            ] = f"Agendamento {self.cleaned_data['data_inicial']}"
        return super().save()


class AtendenteForm(BaseForm):
    """Form padrão para o model Atendente"""

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = Atendente


class AtendimentoForm(BaseForm):
    """Form padrão para o model Atendimento"""

    hora_inicial = forms.TimeField(
        widget=TimePicker(
            options={
                "stepping": 10,
                "format": "HH:mm",
            }
        )
    )

    hora_final = forms.TimeField(
        widget=TimePicker(
            options={
                "stepping": 10,
                "format": "HH:mm",
            }
        )
    )

    data = forms.DateField(
        widget=DatePicker(
            options={
                "minDate": datetime.now().strftime("%Y-%m-%d"),
            }
        )
    )

    class Meta:
        exclude = ["deleted", "enabled", "deleted_on"]
        model = Atendimento

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("hora_final") and not cleaned_data.get("hora_inicial"):
            self.add_error(
                "hora_final", "A hora final e a hora inicial são obrigatórias"
            )

        elif cleaned_data["hora_final"] < cleaned_data["hora_inicial"]:
            self.add_error(
                "hora_final", "Hora final não pode ser menor que hora inicial"
            )

        elif cleaned_data["hora_final"] == cleaned_data["hora_inicial"]:
            self.add_error("hora_final", "Hora final não pode ser igual a hora inicial")
