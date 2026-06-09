# Escondendo campos no Formulário

Por vezes você querá esconder algum campo em seu formulário.

## Forms

1. Em seu arquivo form, import o `Form` do Django

2. Crie a função `__init__`

3. Adicione o campo que quer esconder e atribua seu `widget` ao `HiddenInput`

4. Sua classe Form ficará parecida com esta abaixo

```
from django import forms
...
class SuaClasse():
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['nome_do_campo'].widget = forms.HiddenInput()
```

## O que acontece no HTMl?

Em seu HTML, todas as tags do campo estarão dentro de uma tag `if` que
verifica se seu campo deverá ser exibido ou não por meio do `forms.visible_fields`

```
{% if form.nome_do_campo in form.visible_fields %}
   <div class="form-group col-md-6">
      {{ form.nome_do_campo.label_tag }}
      {{ form.nome_do_campo }}
      <div class="invalid-feedback">
         Campo Requerido.
      </div>
      {% if form.nome_do_campo.errors  %}
         {{ form.nome_do_campo.errors  }}
      {% endif %}
   </div>
{% endif %}
```

O código HTML acima é somente um exemplo e não é preciso adicioná-lo manualmente pois o comando `build` é responsável por isso