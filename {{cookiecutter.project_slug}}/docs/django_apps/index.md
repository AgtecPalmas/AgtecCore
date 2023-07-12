# Novas app do seu projeto

Após a configuração inicial do projeto quando forem criadas novas apps django no projeto, os seguintes passos devem ser
seguidos para que os managers funcionem de forma correta.

### Observação

Não deve ser executado o comando **python manage.py build nome_da_app**, esse comando só deve ser executado dessa forma
logo após a criação inicial do projeto, aonde temos apenas a app usuario.

### Etapas

1. Criar a nova app com o comando **python manage.py startapp nome_da_app**
1. Adicionar a app no **INSTALLED_APPS[...]* do aquivo *settings.py**
1. Criar os models com seus respectivos atributos
    1. Adicionar no class Meta do models os campos que deseja que sejam renderizado no list_view **fields_display =
       ['campo_um', 'campo_n']**
    2. Adicionar no class Meta do models os campos que são do tipo ForeingKey e que você deseja que sejam gerados os
       modais nas telas de inserção de edição do registro ** fk_fields_modal = ['campo_fk_um', 'campo_fk_n'] **

### Exemplo de class Meta configurado:

```python hl_lines="2 3" 
    class Meta:
        verbose_name = 'Nome do Model'
        verbose_name_plural = 'Nome do Model no Plural'
        fields_display = ['campo_um', 'campo_dois', 'campo_n']
        fk_fields_modal = ['campo_fk_um', 'campo_fk_dois', 'campo_fk_n']
```

2. Executar os comandos **python manage.py makemigrations** e **python manage.py migrate**
3. Executar o comando **python manage.py build nome_da_app** com as flags na ordem a seguir:
    1. **python manage.py build nome_da_app --forms** *serão gerados os forms dos models da app informada*
    2. **python manage.py build nome_da_app --views** *serão geradas as views dos models da app informada*
    3. **python manage.py build nome_da_app --urls** *serão geradas as urls dos models da app informada*
    4. ***Agora adicione no arquivos urls.py do projeto (base) o path para as urls da app***
       path('core/', include('nome_da_app.urls', namespace="nome_da_app")),
    5. **python manage.py build nome_da_app --templates** *serão gerados os templates html dos models da app informada*
    1. **python manage.py build nome_da_app --parserhtml** *serão realizados os parser dos templates HTML contendo os
       atributos dos models da app informada*
    1. **python manage.py build nome_da_app --api** *serão gerados os arquivos da APIRest dos models da app informada*
4. Para gerar todos os arquivos com um único comando execute:  
    1. **python manage.py build nome_da_app --all** 

5. Para forçar a geração dos templates mesmo com a tag `#FileLocked` utilize:
    1. **python manage.py build nome_da_app --all --force** 
    1. **python manage.py build nome_da_app --templates --force** 