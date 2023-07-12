from django import forms
from django.forms import TextInput


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


def moneyInput():
    return TextInput(attrs={"input-mask": "money"})
