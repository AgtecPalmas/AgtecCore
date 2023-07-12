# Configurado o Pycharm para executar em modo debug

** Para usuários Windows é necessário garantir que o WSL2 esteja configurado e tenha instalado o Docker Desktop **

A configuração do Pycharm para executar utilizando o docker em modo debug é bem simples, basta seguir os passos abaixo:

### Verificar o Docker
1. Abra as configurações (Settings) do projeto conforme a imagem abaixo
   ![Pycharm Settings](../images/pycharm-docker-config-one.png)
2. Acesse a área de Build, Execution, Deployment > Docker
   ![Pycharm Settings](../images/pycharm-docker-config-two.png)
   ![Pycharm Settings](../images/pycharm-docker-config-three.png) 
   **Caso não apareca o Docker clique no sinal de + e configure o Docker**     

### Adicionar o interpretador Python
1. Na tela de configuração (Settings) clique em adicionar interpretador e escolha a opção ***On Docker Compose*** do projeto conforme a imagem abaixo
   ![Pycharm Settings](../images/pycharm-docker-config-five.png)    
   ![Pycharm Settings](../images/pycharm-docker-config-six.png)    

1. Na janela que aparecerá escolha na opção ***Service*** **web** e clique em ***Next***
      ![Pycharm Settings](../images/pycharm-docker-config-seven.png)
1. Na próxima tela selecione o interpretador recem criado e clique em ***Criar(Create)***
1. Agora é necessário executar o docker-compose para criar o container, para isso basta abrir o arquivo docker-dev.yml e clicar nas duas setas verdes que encontram-se antes do services conforme a imagem abaixo
      ![Pycharm Settings](../images/pycharm-docker-config-eight.png)
### Criando o arquivo de execução 
Agora vamos criar uma configuração do Django Server também na tela de configuração (Settings) do projeto, para isso clique em ***Add Configuration*** conforme a imagem abaixo
![Pycharm Settings](../images/pycharm-docker-config-nine.png)
***A diferença na configuração nessa tela para o que já foi feito é que agora vamos configurar no ***Python Interpreter*** o interpretado que criamos no passo 3***. E depois clicamos em Ok

----
Pronto, agora é só executar o debug e o Pycharm irá executar o projeto dentro do container docker. Desta forma podemos 
utilizar o breakpoint para debugar o código e verificar o que está acontecendo no projeto.

----
## Links
[Jetbrains Docs](https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html)

