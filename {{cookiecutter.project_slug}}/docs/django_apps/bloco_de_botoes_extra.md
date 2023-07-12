# Adicionar botões extras no list_view

1. Por padrão o core ja vem com um bloco de botoes extras, que é o bloco de botoes de ações.
2. Na list view só criar um block barra_botoes_extra e colocar os botoes que deseja.
3. O bloco ja vem com css aplicado para espaçamento e ja vem como ROW por padrão.

exemplo:

## exemple_list.py

    {% block barra_botoes_extra %}
         <a href="{% url 'exemple:exemple_create' %}" class="br-button primary col-2 ">
            <i class="fa fa-plus"></i> Novo
         </a>
    {% endblock barra_botoes_extra %}