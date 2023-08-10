# Projeto Flutter

Esse projeto foi gerado a partir do AgteCore, as configurações iniciais do projeto (CRUD) foram geradas.
Abaixo descrevemos os passos que devem ser seguidos para rodar o projeto.

## Etapas para rodar o projeto

[ ] 1 - Adicionar o multiDexEnabled para poder trabalhar com pacotes maiores de 64K no arquivo, mudar a versão do SDK

```code
build.gradle no caminho android/app/build.gradle e alterar as constantes
  defaultConfig {
    ...
    multiDexEnabled true
    minSdkVersion flutter.minSdkVersion -> minSdkVersion 19
    targetSdkVersion flutter.targetSdkVersion -> targetSdkVersion 30
    ...
}
```

[ ] 2 - Criar o projeto no Firebase [https://firebase.google.com/]
[ ] 3 - Ativar a funcionalidade de autenticacao
[ ] 4 - Baixar o arquivo google
[ ] 5 - Configurar o projeto no Android e iOS para trabalhar com a autenticação, conforme documentação do Flutter
[ ] 6 - Configurar no arquivo lib/core/config.dart a costante uriDeveloper apontando para a URL da API do projeto DRF ou FastAPI
[ ] 7 - Configurar no arquivo lib/core/config.dart a costante DRFToken para o token de ambiente de desenvolvimento.

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
