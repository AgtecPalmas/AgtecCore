# Usando ElasticSearch com Kibana

## ElasticSearch

É um programa gratuito para buscar e analisar dados gigantes em tempo real.
Pode ser usado para pesquisar textos, monitorar logs e mais.
É escalável e muito usado para aplicações de busca e análise de dados.

## Kibana

É uma plataforma de análise e visualização de dados de código aberto que funciona em conjunto com o Elasticsearch.
Ele permite criar gráficos, tabelas, mapas e dashboards interativos para ajudar a entender e explorar dados de forma mais fácil e intuitiva.
É amplamente utilizado para monitorar e analisar dados em tempo real, para investigar problemas em logs de aplicativos e para obter insights em grandes conjuntos de dados.

## Instalação

### Python

 `pip install elastic-apm`

O Core está usando a versão `elastic-apm==6.15.1`


### Django

Crie um arquivo chamado `elastic.py` na pasta `base` e adicione o seguinte conteúdo substituindo `nome_do_projeto`:

Caminho: `projeto/base/elastic.py`


```python
from decouple import config

APP_ID = "nome_do_projeto"

ELASTIC_APM = {
    "SERVICE_NAME": "nome_do_projeto",
    "SERVER_URL": config("ELASTIC_APM_SERVER_URL"),
    "DEBUG": config("DEBUG", default=False, cast=bool),
    "ENVIRONMENT": config("ENVIRONMENT", default="desenvolvimento"),
}
```

Adicione a importação do arquivo criado, o Middleware e o APP no arquivo `settings.py`:

```python
if DEBUG is False:
    ...

    from .elastic import ELASTIC_APM

    INSTALLED_APPS.append("elasticapm.contrib.django")
    MIDDLEWARE.append("elasticapm.contrib.django.middleware.TracingMiddleware")
```

Utilização por padrão dentro do bloco onde o Debug é falso para ser usado apenas em ambientes de produção e homologação.

### Variáveis de ambiente (.env)

Adicione as seguintes variáveis de ambiente no arquivo `.env`:

```bash
ELASTIC_APM_SERVER_URL=http://localhost:8200
ENVIRONMENT=desenvolvimento
```

Configure o nome do ambiente de acordo com o que está sendo usado.
