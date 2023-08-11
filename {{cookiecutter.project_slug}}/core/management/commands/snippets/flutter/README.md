# Projeto Flutter

Esse projeto foi gerado a partir do AgteCore, as configurações iniciais do projeto (CRUD) foram geradas.
Abaixo descrevemos os passos que devem ser seguidos para rodar o projeto.

## Etapas para rodar o projeto

1. Configurando o projeto para executar no Android
1.1 Alterar o versão do compileSdkVersion para **33** no arquivo build.gradle no caminho **android/app/build.gradle**
    ```code
        android {
            compileSdkVersion 33
        ...
    ```
    1.2 Adicionar no arquivo build.gradle no caminho **android/app/build.gradle** o **multiDexEnabled true**
    ```code
        defaultConfig {
            ...
            multiDexEnabled true 
            ...
        }
    ```
    1.3 Alterar no arquivo **android/app/build.gradle** o **minSdkVersion** para **19**
    ```code
        defaultConfig {
            ...    
            minSdkVersion 19
            ...
        }
    ```
    1.4 Alterar no arquivo **android/app/build.gradle** o **targetSdkVersion** para **30**
    ```code
        defaultConfig {
            ...    
            targetSdkVersion 30
            ...
        }
    ```

2. Instalar o FVM para facilitar o trabalho no versionamento das versões do Flutter [https://fvm.app/] (Etapa opcional)
3. Criar o projeto no Firebase [https://firebase.google.com/] (Etapa opcional)
4. Ativar a funcionalidade de autenticacao (Etapa opcional)
5. Baixar o arquivo google (Etapa opcional)
6. Configurar o projeto no Android e iOS para trabalhar com a autenticação, conforme documentação do Flutter (Etapa opcional)
7. Configurar no arquivo lib/core/config.dart a costante uriDeveloper apontando para a URL da API do projeto DRF ou FastAPI
8. Configurar no arquivo lib/core/config.dart a costante DRFToken para o token de ambiente de desenvolvimento.

## O projeto gerado contém as seguinte estrutura

```code
projeto flutter
├── android - diretório padrão do android
├── ios - diretório padrão do ios
├── lang - diretório contendo arquivos de tradução (caso queira utilizar)
│   ├── en.json
│   ├── pt.json
├── lib
│   ├── apps - Diretório contendo as apps do projeto (geradas baseadas no projeto Django)
│   |    ├── auth - App gerada automaticamente para trabalhar com autenticação
│   ├── core - Diretório com apps 'auxiliares' para o projeto
│   |    ├── dio - Classe customizada do pacote Dio
│   |    ├── exceptions - Classe para trabalhar com exceptions customizadas
│   |    ├── extensions
│   |    ├── user_interface - Classes para gerenciamento das cores padrões da app, widget's, font's e style's
│   |    ├── agtec.logger.dart - Classe para geração de log´s
│   |    ├── config.dart - Classe para configuração de constantes utilizadas no projeto
│   |    ├── localization.dart - Classe responsável pela configuração da localização para trabalhar com internacionalização
│   |    ├── util.dart - Classe com funções úteis como converção de datas, geração de dados mocados para o desenvolvimento, etc
│   |── home.page.dart - arquivo com crud padrão a ser herdados
|   |── main.dart - arquivo de configuração  do banco de dados
|   └── routers.dart - arquivos de configuração de seguranca
├── .flutter-plugins - arquivo gerado automaticamente pelo flutter
├── .flutter-plugins-dependencies  - arquivo gerado automaticamente pelo flutter
├── .gitignore
├── .metadata
├── analysis_options.yaml  - arquivo gerado automaticamente pelo flutter
├── doctorweb.iml
├── pubscpec.lock  - arquivo gerado automaticamente pelo flutter
├── pubscpec.yaml - arquivo gerado automaticamente pelo flutter
└── README.md

```

----

## Documentação

<https://agtecpalmas.github.io/AgtecCore/>
