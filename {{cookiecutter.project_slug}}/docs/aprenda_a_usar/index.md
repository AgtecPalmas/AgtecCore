# Projeto Django

Esse projeto foi criado utilizando o AgtecCore, que gera um projeto Django com as configurações utilizadas normalmente em projetos, com Django Rest Framework e com managers que auxiliarão no desenvolvimento do seu projeto.

> Lembre-se de sempre consultar a documentação quando surgir alguma dúvida.

## Instalação
Abaixo temos as etapas a serem executadas quando o projeto for criado.

### Ativar o virtualenv

    .\.venv\Script\activate | windows
    . venv/bin/activate | linux e macOs

### Comandos a serem executados após a criação do projeto

1. Acessar o subdiretório do projeto que foi criado após o comando *cookiecutter ..\agteccore*
1. Gerar a secret_key do projeto Django.
    1. Abra o terminal.
    2. Ative o ambiente virtual
    3. Execute os comando a seguir.

O código gerado deve ser colocado no arquivo .env que contêm os parâmetros de configuração do projeto.

```console
python contrib/secret_gen.py
```

1. Instale as dependências  
   ```pip install -r requirements.txt```   
   ```pip install -r requirements-dev.txt```
2. Execute o comando de criação das migrações  
   ```python manage.py makemigrations```
3. Execute o comando de aplicação das migrações    
   ```python manage.py migrate```
4. Crie os códigos boilerplates da app usuario  
   ```python manage.py build usuario --all```
5. Crie os códigos boilerplates da app configuracao_core  
   ```python manage.py build configuracao_core --all```
6. Crie o super user padrão do projeto  
   ```python mock_superuser.py```
7. Crie usuários de exemplo da app usuário  
   ```python mock_data.py```

-----

Esse projeto já traz por padrão a app de Usuario/usuario. Ao executar o comando migrate já foi adicionado no banco de
dados as tabelas relativas a essa app, agora é necessário executar o comando abaixo para que os arquivos boilerplates da
app/model sejam criados.

Com o comando de criação do superusuário temos um usuário do tipo SuperUser com os dados abaixo.

    login: admin  
    senha: senha_padrao_deve_ser_mudada  
    DRF Token: 2b817ddbb5b974e5a451a8156963de586d72079e


## Comandos do Core

Você pode executar dois comandos internos do Core

### --version

Esse comando exibe a versão do Core que está sendo utilizada no projeto.

```console
python manage.py core --version
```
```console
✅  Versão do Core: 4.2.1
```

### --upgrade

Esse comando verifica se existe uma nova versão do Core disponível e pergunta se deseja atualizar.
Toda a pasta Core será substituida pela nova versão, lembre-se de verificar se você fez alguma alteração no Core antes de atualizar.
Se novas variáveis forem adicionadas ao Core, elas serão inseridas no base/settings.py automaticamente, mas sem valor.

```console
python manage.py core --upgrade
```

```console
🆙  Atualização 4.3 disponível
Versão 4.2.1 está sendo usada

Baixar atualização
https://github.com/agtec//releases/tag/4.3
Deseja atualizar o Core? [S/N]
```