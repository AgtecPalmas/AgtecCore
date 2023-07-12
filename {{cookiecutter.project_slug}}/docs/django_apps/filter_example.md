# Aplicando filtro e criando o arquivo filter.py

1. Criar um arquivo filter.py na app requerida para configuração do modulo django_filters. De prefêrencia criar o
   arquivo no mesmo nivel a qual ele vai ser importado.

2. No arquivo filter.py importar os models que deseja aplicar o filtro.

3. Criar a classe filter para o model desejado ( Ex: se o model é Exemplo, criar FilterExemplo)

4. Na classe filter, criar a classe meta para apontar pro model e definir os campos que serão utilizados para filtragem.

5. Caso deseja personalizar o filtro, como por exemplo, definir label, adicionar atributos e outros comportamentos,
   deverá definir dentro do metodo __init__, lembrando de definir separado para cada campo/filtro.

exemplo:

## filter.py

    import django_filters

    from exemplo.models import Exemplo

    class ExemploFilter(django_filters.FilterSet):
        class Meta:
            model = Exemplo
            fields = ['nome','cpf', 'email']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.filters["nome"].lookup_expr = 'icontains'
            self.filters["nome"].label = 'Nome'

            self.filters["cpf"].lookup_expr = 'icontains'
            self.filters["cpf"].label = 'CPF'

            self.filters["email"].lookup_expr = 'icontains'
            self.filters["email"].label = 'Email'

## Importando o filtro na views

1. Na view, importar do filter.py o filtro especifico que vai utilizar na view.

2. Importar também do django_filter.views o FilterView.

3. A classe que vai utilizar o filtro, vai herdar o FilterView. (Coloque Filter no nome da classe para melhor
   visualização ( ExempleFilterView ))

4. Dentro da classe que herdou o FilterView, junto com o padrão Class Base View, declare filterset_class recebendo o
   filtro que foi importando do arquivo filter.py.    
   (filterset_class = ExempleFilter)

Exemplo:

    from django_filters.views import FilterView

    class ExemploListView(FilterView):
        """Classe para gerenciar a listagem do Exemplo"""

        model = Exemplo
        template_name = "usuario/exemplo_listfilter.html"
        context_object_name = 'exemplo'
        list_display = ['nome', 'email', 'cpf'']
        filterset_class = ExemploFilter

## No arquivo html

1. No arquivo html o filtro vem pela tag filter.

2. A tag filter tem que ser utilizada dentro da tag html de form para funcionar.

3. Por padrão ela não vem com um botão para submit, só vem com os inputs e labels.

4. Pode ser utilizado filter.form que vai herdar o css geral caso utilize template, ou filter.form.as_p
   que vai renderizar o form basico mais oque for configurado no arquivo filter.py no metodo init.

5. Também pode só chamar um input de filtragem especifico, chamando filter.form."campo" (exemplo: filter.form.nome), e
   tambem chamar só o label. filter.form."campo".label

Exemplo:

```
<form method="get" >
    <div class="row">

        # chamado o formulario de filtro baseado na classe meta (o css vai vir herdada do template)
        {{ filter.form }}

        # chamado o formulario de filtro baseado no metodo __init__(o css sera basico e vai ter q fazer manualmente)
        {{ filter.form.as_p }}

        # somente o input de nome
        {{ filter.form.nome }}

        # somente o label de nome
        {{ filter.form.nome.label }}

        <div class="col-2">
            <button class="btn btn-success form-control" type="submit">Buscar</button>
        </div>
        
    </div>
</form>
```
