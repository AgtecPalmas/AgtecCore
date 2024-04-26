from django_select2 import forms as s2forms


class CoreMultipleSelect2Widget(s2forms.ModelSelect2MultipleWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["data-minimum-input-length"] = 0
        self.attrs["style"] = "width: 100%"
        self.attrs["data-theme"] = "bootstrap-5"
        self.attrs["data-placeholder"] = "Buscar itens"


class CoreSelect2Widget(s2forms.ModelSelect2Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["data-minimum-input-length"] = 0
        self.attrs["style"] = "width: 100%"
        self.attrs["data-theme"] = "bootstrap-5"
        self.attrs["data-placeholder"] = "Buscar itens"
