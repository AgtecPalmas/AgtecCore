# Templates HTML

Caso seja necessário customizar algo no template HTML abaixo temos as instruções de como proceder

## Importando arquivo js

1. Na view, importar do filter.py o filtro especifico que vai utilizar na view.

2. Importar também do django_filter.views o FilterView.

3. A classe que vai utilizar o filtro, vai herdar o FilterView. (Coloque Filter no nome da classe para melhor
   visualização ( ExempleFilterView ))

4. Dentro da classe que herdou o FilterView, junto com o padrão Class Base View, declare filterset_class recebendo o
   filtro que foi importando do arquivo filter.py.    
   (filterset_class = ExempleFilter)

Exemplo:

    from django_filter.views import FilterView

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
