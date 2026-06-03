# Aplicando filtros com django_filters

Caso você queira utilizar filtros em uma listagem de um model, você pode utilizar o django_filters.


## Como funciona?

O django_filters é um modulo que permite a criação de filtros para os models, com ele é possível criar filtros para os campos do model, e aplicar esses filtros na listagem do model ou em qualquer outra view que desejar.

## Configurando o Filter

Crie um arquivo filters.py na app requerida para configuração do modulo django_filters.

```python
from django import forms
from django_filters import filterset

from .models import Livro


class LivroFilter(filterset.FilterSet):

    titulo = filterset.CharFilter(
        label="Titulo",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    autor = filterset.CharFilter(
        label="Autor",
        method="filter_autor",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    created_at = filterset.DateFilter(
        label="Criado depois de",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    def filter_autor(self, queryset, name, value):
        return queryset.filter(autor__nome__icontains=value)

    class Meta:
        model = Livro
        fields = ["titulo", "autor", "created_at"]
```

Lembre-se sempre de utilizar o `lookup_expr` corretamente para definir o tipo de filtro que será aplicado, como no exemplo o `icontains` que é um filtro de texto que busca por parte do texto e o `gte` que busca por datas maiores ou iguais.

Se necessário uma filtragem mais complexa, é possível criar filtros customizados, como no exemplo o `filter_autor`.

Você é capaz de passar atributos comuns de um form, como label, widget, required, etc.


## Configurando a View

Sua view deverá herdar de `django_filters.views.FilterView` e definir o atributo `filterset_class` com o filtro que você criou.

```python
from django_filters.views import FilterView

from teste_livro.filter import LivroFilter
from teste_livro.models import Livro


class LivroListView(FilterView, BaseListView):
    ...
    model = Livro
    filterset_class = LivroFilter
```

## Configurando o Template

Os templates list do Core já possuem uma verificação para renderizar o filtro corretamente.

Mas se for necessário utilizar o filtro em outro template, é necessário renderizar o filtro manualmente.
Use `filter.form` ou `filter.form.as_p` no template.

Segue um exemplo de como utilizar o filtro no template:

```html
<form method="get">
    <div class="d-flex flex-column flex-md-row justify-content-start mb-4 gap-large">
        {% for filtro in filter.form %}
            <div class="form-floating">
                {{ filtro }}
                {{ filtro.label_tag }}
            </div>
        {% endfor %}
        <div class="align-self-center">
            <button class="br-button secondary block" type="submit">
                <i class="fas fa-filter mr-2"></i> Filtrar
            </button>
        </div>
    </div>
</form>
```

# Leia mais

Acesse a [documentação oficial](https://django-filter.readthedocs.io/en/main/guide/usage.html#the-filter) para mais informações sobre o django_filters.
