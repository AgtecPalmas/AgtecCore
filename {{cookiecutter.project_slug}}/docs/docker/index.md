# Como utilizar

Abaixo listamos os comandos para executar o projeto utilizando Docker e também os comandos para que seja possível depois
do container subir executar os comandos dentro da imagem.

Para usuários Windows é necessário garantir que o WSL2 esteja configurado e tenha instalado o Docker Desktop

### Criando a imagem e executando o container

    docker-compose up -d

### Executando em ambiente de desenvolvimento

    docker-compose --f docker-dev.yml up -d

### Forçando a geração da nova imagem e container

    docker-compose -f docker-dev.yml up -d --force-recreate --no-deps

### Mostrando as imagens geradas

    docker image ls

Após a execução do comando acima deve ser mostrado no terminal o nome das imagens que foram criadas, uma das imagens é o
banco de dados, e outra é o projeto (web) que traz o mesmo nome do seu projeto, para os demais comandos é necessário
copiar o IMAGE ID do projeto, que no exemplo abaixo é **55c290edebcd**

````
REPOSITORY               TAG           IMAGE ID       CREATED          SIZE
NOME_DO_SEU_PROJETO      latest        55c290edebcd   40 minutes ago   880MB
docker/getting-started   latest        bd9a9f733898   7 weeks ago      28.8MB
postgres                 13.4-alpine   682810fa689e   5 months ago     192MB
````

### Mostrando os containers

    docker container ls

Após a execução do comando acima deve ser mostrado no terminal os containers que foram criados.
O container que roda a aplicação django terá um nome parecido com NOME_DO_SEU_PROJETO_web_1, no exemplo abaixo é
é **agtectcore_web_1**

````
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                    NAMES
b3097cb73d33   agtectcore       "bash -c 'python man…"   7 minutes ago   Up 7 minutes   0.0.0.0:8000->8000/tcp   agtectcore_web_1
46d23ebe2f9b   postgres:14.3   "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes   5432/tcp                 agtectcore_database_1
````
Para executar os comandos no container basta utilizar o comando abaixo:

    docker exec -it agtectcore_web_1 COMANDO_QUE_DESEJA_EXECUTAR

### Abrindo o shell no container

    docker exec -it CONTAINER_ID sh

Com esse comando o terminal passa a ser de dentro do container

### Para sair do shell do container sem derrubar o container basta utilizando o conjunto de teclas

    CTRL + P , CTRL + Q

### Criando a SECRET_KEY

    docker exec -it agtectcore_web_1 sh -c "python contrib/secret_gen.py"

O comando acima retorna uma string similar a esta
***gvN3L7UR_4ADJrUjnLGdjzZuvFoT01gqYyFfQkY0Qava7DigkWS63YP8UBl7saAcV3E*** essa string é a chave secreta que será utilizada pelo Django para gerar as senhas e deve ser adicionada como variável de ambiente no arquivo Dockerfile.Dev

### Executando o makemigrations

    docker exec -it agtectcore_web_1 sh -c "python manage.py makemigrations"

### Executando o migrations

    docker exec -it agtectcore_web_1 sh -c "python manage.py migrate"    

### Executando o build da app Usuario

    docker exec -it agtectcore_web_1 sh -c "python manage.py build usuario"

### Executando o comando para gerar o SuperUser

    docker exec -it agtectcore_web_1 sh -c "python mock_superuser.py"

### Executando o comando para gerar os dados Fake do models Usuario

    docker exec -it agtectcore_web_1 sh -c "python mock_data.py"

### Criando uma nova app

    docker exec -it agtectcore_web_1 sh -c "python manage.py startapp NomeDaNovaApp"
