
# Alembic

Alembic é um pacote responsável pela gestão de migrações de banco de dados em aplicações Python.

## Instalação

Instale o pacote Alembic usando o seguinte comando:

```
pip install alembic
```

## Configuração

Gere um arquivo de configuração para o Alembic:

```
alembic init alembic
```

Isso criará um diretório chamado "alembic" com arquivos de configuração.

### Configurando arquivo env.py

Dentro do diretório "alembic" no arquivo env.py. Nesse caso, essas configurações fazem necessárias, pois é usado o comando [`autogenerate`](#executando-migrações) para gerar o arquivo de migração.

#### 1. Configurando a URL do banco de dados:

    from core.database import SQLALCHEMY_DATABASE_URI 
    config = context.config
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)
    

#### 2. Importar os models da API:


    import importlib

    models = [
        'app.modulo.models.NomeModels',
    ]

    for model in models:
        try:
            model_path, class_name = model.rsplit('.', 1)
            module = importlib.import_module(model_path)
        except ImportError:
            print(f"Error importing model: {model}")


#### 3. Definindo o Metadata dos models:

    
    from core.database import Base
    target_metadata = Base.metadata
    

#### 4. Incluindo apenas tabelas dos módulos mapeados:

    def include_name(name, type_, parent_names):
        if type_ == "table":
            return name in target_metadata.tables
        return True
    

E na função `run_migrations_online` (gerada pelo alembic), adicione a função `include_name`, como:

  
    def run_migrations_online():
        ...
        with connectable.connect() as connection:
                context.configure(
                    ...
                    include_name=include_name,
                    ...
                )
    

#### 5. Omitir models do processo de migração:

  
    def include_object(object, name, type_, reflected, compare_to):
        if object.info.get("skip_autogenerate", False):
            return False
        return True
  

E também inclua `include_object=include_object` na função `run_migrations_online`, por exemplo: 

    
    def run_migrations_online():    
        ...
        with connectable.connect() as connection:
                context.configure(
                    ...
                    include_object=include_object,
                    ...
                )
  

### Omitindo models na migração

Por exemplo, se você não quiser incluir o model de Usuário, adicione o seguinte código:


    class Usuario(CoreBase):
        __table_args__ = {'info': {'skip_autogenerate': True}}
     ...

e certifique de ter implementado, também, o seguinte código no [item 5](#configurando-arquivo-envpy).

### Executando migrações (Comandos)

#### 1. Criando migrações:

   Gerando arquivo de migração automaticamente baseado nos models identificados no [item 3](#configurando-arquivo-envpy).

    
    alembic revision --autogenerate -m "nome_da_migracao"
    

#### 2. Aplicando as migrações sem `autogenerate`:
Gera um arquivo de migração que manualmente pode ser alterado adicionando alterações de downgrade e upgrade.
        
    alembic revision -m "nome_da_migracao"
        
#### 3. Aplicando as migrações:

    alembic upgrade head
        

#### 4. Desfazendo migração:

Para desfazer a última migração use:

    
    alembic downgrade -1
     

Para desfazer uma migração específica:

    
    alembic downgrade nome_da_migração

???+ note

    
    Sugerimos que os nomes dos arquivos de migração tenham alguma forma de identificar a ordem das migrações, no seguinte padrão:  
    ```  
    chave-migração_numero-da-migração_nome.py
    ```
    Por exemplo:    
    ```
    8380654eebbd_third_migration_data-user.py
    ```
    a chave de migração é gerada automaticamente pelo Alembic.


### Documentação Alembic

Para obter mais informações consulte a [documentação do Alembic](https://alembic.sqlalchemy.org/en/latest/)