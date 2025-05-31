# Projeto Flutter

Esse projeto foi gerado a partir do NuvolsCore, as configurações iniciais do projeto (CRUD) foram geradas.
Abaixo descrevemos os passos que devem ser seguidos para rodar o projeto.

# Versão do Flutter

#### Esse projeto foi gerado usando as versões:

Dart: 3.7.2
Flutter: 3.29.3
DevTools: 2.42.3

# Integração com a camada de API, projeto Django ou FastAPI

Por padrão todos os endpoint's das API's necessitam de autenticação, caso 
deseje desenvolver sem a necessidade de autenticar, acesse os projetos Django/FastAPI e desabilite a autenticação.

## Dica de linter para o projeto

Como forma de auxiliar no desenvolvimento do projeto, recomendamos aplicar as regras de linter no projeto, caso o build não tenha alterado o arquivo copie o código abaixo e cole no arquivo **analysis_options.yaml** que fica na raiz do projeto e adicionar as regras abaixo:

```yaml
...
  rules:
    avoid_print: true
    prefer_single_quotes: true
    prefer_final_locals: true
    prefer_relative_imports: true
    dangling_library_doc_comments: false
```

## Etapas para rodar o projeto

1. Criar um repositório git
2. Configurando o projeto para executar no Android 
    
    2.1 Adicionar no arquivo build.gradle no caminho **android/app/build.gradle.kts** para **23**
    ```code
        defaultConfig {
          ... 
           minSdk = 23
          ...
        }
    ```

1. Instalar o FVM para facilitar o trabalho no versionamento das versões do Flutter [https://fvm.app/] (Etapa opcional)
2. Configurar o VsCode para executar o Flutter do FVM [https://fvm.app/docs/getting_started/configuration] (Etapa opcional)
3. Criar o projeto no Firebase [https://firebase.google.com/] (Etapa opcional)
4. Ativar a funcionalidade de autenticacao (Etapa opcional)
5. Baixar o arquivo google (Etapa opcional)
6. Configurar o projeto no Android e iOS para trabalhar com a autenticação, conforme documentação do Flutter (Etapa opcional)
7. Configurar no arquivo lib/core/config.dart a costante uriDeveloper apontando para a URL da API do projeto DRF ou FastAPI
8. Configurar no arquivo lib/core/config.dart a costante drfToken para o token de ambiente de desenvolvimento.

```dart
void main() async {
    /// [FirebaseRemoteConfig]
    /// Para habilitar o acesso ao Firebase Remote Config
    /// faça as configurações necessárias conforme a documentação do Firebase,
    /// https://firebase.google.com/docs/flutter/setup?hl=pt-br&platform=ios
    /// e depois descomente a linha abaixo.
    /// await ApplicationConfig().config();
    runApp(MyApp());
}
```

## O projeto gerado contém as seguinte estrutura

```code
projeto flutter
├── android - diretório padrão do android
├── ios - diretório padrão do ios
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
├── NOME_DO_PROJETO.iml
├── pubscpec.lock  - arquivo gerado automaticamente pelo flutter
├── pubscpec.yaml - arquivo gerado automaticamente pelo flutter
└── README.md

```

----

## Documentação

<https://agtecpalmas.github.io/NuvolsCore/>
