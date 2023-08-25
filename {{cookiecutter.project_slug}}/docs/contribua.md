# Como contribuir

Obrigado por se interessar em contribuir no nosso projeto! Nesse documento há instruções sobre como fazer isso

## Funcionamento do AgtecCore

### Estrutura do projeto

> Todo: detalhar a estrutura e como o projeto funciona


## Passo a passo para contribuir

Há várias formas de contribuir com o projeto, com código, testes, documentação, etc. Nesse documento, vamos mostrar uma forma de contribuir com o projeto, mais especificamente com a documentação. Para isso, vamos seguir os passos abaixo:

### Faça um fork da branch `desenvolvimento`

Para contribuir com o projeto, você deve fazer um fork da branch `desenvolvimento` do projeto. Para isso, na [página do projeto](https://github.com/AgtecPalmas/AgtecCore/tree/desenvolvimento), basta clicar no botão `Fork` no canto superior direito da tela.
> Lembre-se de fazer o fork da branch `desenvolvimento` e não da `main`.

![Fork](./images/fork.png)

### Clone o fork para sua máquina local

Você deve clonar o fork para sua máquina local. Para isso, basta copiar o link do seu fork e executar o comando `git clone <link_do_fork>`.

### Inicie um projeto com o AgtecCore


Inicialmente, você deve fazer as alterações em um projeto gerado com o AgtecCore e, assim que finalizar, verifique o resultado das alterações. Se estiver tudo certo, transcreva as alterações para o seu fork. Esse processo é necessário pois, para ver o resultado das alterações, você deve rodar a documentação do projeto localmente e isso só é possível se você tiver um projeto gerado com o AgtecCore. Para iniciar um projeto com o AgtecCore, siga o passo a passo do [readme](https://github.com/AgtecPalmas/AgtecCore/#readme) do projeto.
> Sugerimos esse processo pois, caso você faça as alterações diretamente no seu fork, não será tão simples de ver o resultado das alterações em tempo real. 


### Rode a documentação localmente

Com o novo projeto iniciado e com todas as dependências instaladas, você deve rodar a documentação localmente. Para isso, na pasta do projeto, execute o comando `task docs`. Ou se preferir, você pode usar o comando `mkdocs serve`.

### Faça suas alterações

Faça as alterações que deseja na documentação. Para isso, basta editar os arquivos na pasta `docs`. 

### Veja o resultado das suas alterações

Para visualizar o resultado das suas alterações em tempo real, basta acessar o endereço `http://localhost:8000` no seu navegador.
> Lembre-se que o comando `task docs` ou `mkdocs serve` deve estar rodando para ver o resultado das suas alterações.

### Transcreva as alterações para seu fork

Após finalizar suas alterações na pasta `docs` do projeto iniciado com o Agtec Core, você deve transcrever elas para a pasta `{{cookiecutter.project_slug}}/docs` do seu fork. Pois é essa pasta que contém arquivos markdown que são usados para gerar a documentação do projeto. Segue abaixo um exemplo de como fazer isso:

#### Transcreva suas alterações

Na branch `desenvolvimento` do seu fork, transcreva suas alterações feitas na pasta `docs` do projeto iniciado com o Agtec Core para a pasta `{{cookiecutter.project_slug}}/docs` do seu fork. 

#### Commit suas alterações

Após realizar suas alterações, você deve fazer o commit delas. Para isso, basta executar o comando `git commit -m "<mensagem_do_commit>"`.
> Lembre-se de seguir as boas práticas de commit, indicamos o uso dos [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

#### Faça um push das suas alterações

Após realizar o commit das suas alterações, você deve fazer um push delas. Para isso, basta executar o comando `git push origin <nome_do_branch>`.


#### Atualize seu fork fazendo um git pull

Antes de abrir um Pull Request, você precisa garantir que seu fork está atualizado com a branch `desenvolvimento` do projeto AgtecCore, pois neste meio tempo pode ter ocorrido alguma alteração nessa branch, gerando conflitos com suas alterações. Para que isso não ocorra, basta atualizar seu fork executando o comando `git pull upstream desenvolvimento`.

### Abra uma Pull Request (PR)

Após adicionar as alterações no seu fork e atualizar a branch, você deve abrir um Pull Request para a branch `desenvolvimento` do projeto AgtecCore. Para isso, basta clicar no botão `Compare & pull request` ou `Open pull request` no seu fork.
> Lembre-se de confirmar se a PR está sendo aberta da branch `desenvolvimento` do seu fork para a branch `desenvolvimento` do projeto AgtecCore.

> Lembre-se também de fazer a pull para atualizar seu fork antes de abrir a PR.

![Pull Request](./images/pull_request.png)

### Aguarde a revisão da sua PR

Após abrir a Pull Request, você deve aguardar a revisão da mesma. Caso seja necessário realizar alguma alteração, realize-as e faça um novo commit, push e PR.


## Tarefas a serem feitas

Abaixo estão listadas algumas tarefas que precisam ser feitas e que você pode contribuir. 
> Caso queira contribuir com alguma tarefa que não esteja listada aqui, você pode abrir uma [issue no projeto](https://github.com/AgtecPalmas/AgtecCore/issues) relatando o que deseja fazer.


### Documentação

- Documentar esse arquivo (adicionando tarefas a serem feitas, detalhando melhor a estrutura do projeto, etc)
- Documentar tasks do projeto (task docs, task test, task build, etc)
- Documentar como implementar select2
- Documentar como implementar inline formsets

### Testes
- ...

### Implementações
- ...

### Outras
- ...