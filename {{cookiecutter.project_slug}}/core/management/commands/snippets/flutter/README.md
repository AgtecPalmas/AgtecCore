# Projeto Flutter

Esse projeto foi gerado a partir do AgtecCore, as configurações iniciais do projeto (CRUD) foram geradas.
Abaixo descrevemos os passos que devem ser seguidos para rodar o projeto.

# Versão do Flutter

#### Esse projeto foi gerado e validado utilizando a versão do 3.13.0 do Flutter.
```code
PS C:\Users\Suporte> flutter doctor -v
[✓] Flutter (Channel stable, 3.13.0, on Microsoft Windows [versÆo 10.0.22621.2134], locale pt-BR)
    • Flutter version 3.13.0 on channel stable at C:\Flutter\flutter
    • Upstream repository https://github.com/flutter/flutter.git
    • Framework revision efbf63d9c6 (2 days ago), 2023-08-15 21:05:06 -0500
    • Engine revision 1ac611c64e
    • Dart version 3.1.0
    • DevTools version 2.25.0
```

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
    
    2.1 Adicionar no arquivo build.gradle no caminho **android/app/build.gradle** o **multiDexEnabled true**
    ```code
        defaultConfig {
            ...
            multiDexEnabled true 
            ...
        }
    ```

    2.2 Alterar o arquivo build.gradle no caminho **android/build.gradle** para a versão '1.9.10' do kotlin
    ```code
        buildscript {
           ext.kotlin_version = '1.9.10'
           ...
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
    /// Descomentar as linhas abaixo para inicializar o Firebase
    
    // WidgetsFlutterBinding.ensureInitialized();
    // await Firebase.initializeApp();
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

<https://agtecpalmas.github.io/AgtecCore/>
