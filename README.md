*Esta ferramenta digital faz parte do catálogo de ferramentas do **Banco Interamericano de Desenvolvimento**. Você pode saber mais sobre a iniciativa do BID em [code.iadb.org](https://code.iadb.org)*

<h1 align="center"> Agtec Core</h1>
<p align="center"><img src="./images/agtec_core.png"></p>

## Tabela de conteúdos:
---

- [Tabela de conteúdos:](#tabela-de-conteúdos)
- [Informações](#informações)
- [Descrição e contexto](#descrição-e-contexto)
- [Documentação](#documentação)
- [Documentação Externa](#documentação-externa)
- [Guia de instalação](#guia-de-instalação)
- [Dependências](#dependências)
- [Como contribuir](#como-contribuir)
- [Estrutura do projeto gerado](#estrutura-do-projeto-gerado)
- [Autor(es)](#autores)
  - [Coordenador](#coordenador)
    - [Guilherme de Carvalho Carneiro](#guilherme-de-carvalho-carneiro)
  - [Desenvolvedores](#desenvolvedores)
    - [Thiago Schuch](#thiago-schuch)
    - [Claysllan Ferreira](#claysllan-ferreira)
    - [Brayan Mota](#brayan-mota)
    - [Lucas Siqueira](#lucas-siqueira)
    - [Robson Ronzani](#robson-ronzani)
    - [Emanoel Mendes](#emanoel-mendes)
    - [Thales Barbosa](#thales-barbosa)
    - [Márcio Henrique Rodrigues de Lima](#márcio-henrique-rodrigues-de-lima)
    - [Clazzeani Almeida](#clazzeani-almeida)
    - [André Praça de Almeida Pinheiro](#andré-praça-de-almeida-pinheiro)
    - [Marco Antônio Martins Porto Netto](#marco-antônio-martins-porto-netto)
- [Licença](#licença)

## Informações
---
- Dependências de Terceiros: ![dependencies](https://img.shields.io/badge/dependencies-out%20of%20date-orange)
- [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=agtecPalmas_agtecCore&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=agtecPalmas_agtecCore)

  ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![Django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
  ![Postgres](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

## Descrição e contexto
---
Esse projeto foi desenvolvimento para facilitar o desenvolvimento de sistemas Django trazendo diversas tecnologias embarcadas para expandir o conceito Don't Repeat Yourself (DRY). Além das tecnologias já embarcadas, temos managers para automatizar a geração de código do projeto.

## Documentação
___

Utilizamos no desenvolvimento da ferramenta o pacote [mkdocs](https://www.mkdocs.org/), para gerar a documentação do projeto, acesse o site do mkdocs para maiores informações.

## Documentação Externa
---
Acesse a documentação contendo todos os detalhes do projeto em: 
<https://agtecpalmas.github.io/AgtecCore/>

 
## Guia de instalação
---

- Clone este projeto
```
git clone https://github.com/agtec/
```

- Crie um diretório para o seu projeto fora do Clone
```
mkdir <nome_do_seu_projeto>
```

- Acesse o diretório criado na etapa anterior

```
  cd <nome_do_seu_projeto>
```

- Crie e ative um ambiente virtual python (Exemplo)
```
  python3 -m venv venv
  source venv/bin/activate
```

- Atualize o PIP (Recomendado)
````
  python3 -m pip install --upgrade pip
````

- Instale o **cookiecutter**
````console
  pip install cookiecutter==2.3.0
````

- Inicie o projeto com o Cookiecutter apontando para o Clone do Agtec Core
```
cookiecutter <caminho_para_o_clone>/AgtecCore
```

- Siga os passos informados no terminal
  
  <img src="./images/cookiecutter.png">

- Configure seu arquivo .env com as informações do seu banco de dados

- Execute as migrações
```
python3 manage.py makemigrations
python3 manage.py migrate
```

- Crie um super usuário
```
python3 mock_superuser.py
```

- Execute o projeto
```
python3 manage.py runserver
```

---

- Caso o processo do Cookiecutter não tenha sido concluído corretamente, execute os comandos abaixo para instalar as dependências do projeto
```
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt
```

- Construa as aplicações iniciais
```
python3 manage.py build usuario --all
python3 manage.py build configuracao_core --all
```

## Dependências
---
Principais dependências do projeto:

    # Produção
    Django
    Django Rest Framework
    PsyCopg
    Sentry
    ...

    # Desenvolvimento
    Black
    Djlint
    Mkdocs
    Pytest
    Rich
    Taskipy
    ...



## Como contribuir
---
Há várias formas de contribuir com o projeto, com código, testes, documentação, etc.
Acesse a documentação externa na seção [Documentação Externa](#documentação-externa) para saber mais sobre como contribuir com o projeto.


## Estrutura do projeto gerado
---

```mermaid
flowchart TD
    A[ AgtecCore - Cookiecutter ]
A --> B( cookiecutter.. /AgteCore )
B --> D[ Projeto Django baseado no AgteCore]
D --> E[ Projeto Django ]
E --> F( settings.py )
E --> G( urls.py )
E --> H( wsgi.py )
E --> I( manage.py )
I --> T([ build ])
I --> U([ fastapi])
I --> v([ flutter ])
E --> J[ apps ]
J --> K[ atendimento ]
J --> M[ core ]
J --> N[ configuracao_core ]
J --> O[ contrib ]
J --> S[ usuario ]
E --> P[ base ]
E --> Q[ contrib ]
E --> R[ docs]
T --> X( forms.py )
T --> Y( models.py )
T --> Z( views.py )
T --> AA[ templates ]
subgraph " "
AA --> AB( index.html )
AA --> AC( create.html )
AA --> AD( detail.html )
AA --> AE( update.html )
AA --> AF( delete.html )
end

```


## Autor(es)
---
### Coordenador

#### Guilherme de Carvalho Carneiro

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/GCarneiro)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/guilhermecarvalhocarneiro)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/guilhermecarvalho/)

### Desenvolvedores

#### Thiago Schuch

[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/thigschuch)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/thigschuch)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/thiago-schuch)

#### Claysllan Ferreira

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://www.twitter.com/claysllanxavier/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/claysllanxavier)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/claysllanxavier/)

#### Brayan Mota

[![Twitter](https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/brayan_ncm)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BrayanMota)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/brayan-mota)
[![Instagram](https://img.shields.io/badge/instagram-%23E4405F.svg?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/brayanmotaa/)

#### Lucas Siqueira

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lucas-siqueira)

#### Robson Ronzani

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ronzani)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/robson-ronzani/)

#### Emanoel Mendes

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emanoelmendes2)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/emanoel-mendes/)
[![Instagram](https://img.shields.io/badge/instagram-%23E4405F.svg?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/emmmagalhaes/)

#### Thales Barbosa

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/tbblack)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/thales-barbosa-de-oliveira/)

#### Márcio Henrique Rodrigues de Lima

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marciohr9)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/m%C3%A1rcio-henrique-rodrigues-de-lima-71b08576/)

#### Clazzeani Almeida

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/clazzeani)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/clazzeani-almeida-a8a9bb42/)

#### André Praça de Almeida Pinheiro

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/apracapinheiro)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/andr%C3%A9-pinheiro-03064120/)

#### Marco Antônio Martins Porto Netto

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Tchez)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tch%C3%AA/)


## Licença
---

The MIT License (MIT)

Copyright © 2023 Agtec

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-----------------

[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)
