from django.db.models import CharField
from django_select2 import forms as s2forms


class CoreSelect2AbstractWidget:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["data-minimum-input-length"] = getattr(
            self, "minimum_input_length", 0
        )
        self.attrs["data-theme"] = "bootstrap-5"
        self.attrs["data-placeholder"] = getattr(self, "placeholder", "Buscar itens")
        self.attrs["style"] = getattr(self, "style", "width: 100%")
        self.search_fields = self.search_fields or [
            f"{field.name}__icontains"
            for field in self.model._meta.fields
            if isinstance(field, CharField)
        ]

    class Meta:
        abstract = True


class CoreMultipleSelect2Widget(
    CoreSelect2AbstractWidget, s2forms.ModelSelect2MultipleWidget
): ...


class CoreSelect2Widget(CoreSelect2AbstractWidget, s2forms.ModelSelect2Widget): ...
