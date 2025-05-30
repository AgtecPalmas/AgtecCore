# Projeto Flutter

O NuvolsCore possue um manager que gera um projeto flutter já integrado com a camada de API do projeto Django.

## Para que o manager do projeto flutter funcione corretamente é necessário validar as etapas abaixo

1. Verificar se na sua máquina estão instalados o Dart e o Flutter nas versões mínimas abaixo:
    1. Dart 2.16.2
    2. Flutter 2.10.4
    3. Android SDK version 32.1.0-rc1
2. Configurar as apps que serão mapeadas para gerar o projeto Flutter no arquivo setting.py app base
    1. **FLUTTER_APPS = ['usuario', ]**
    2. **Configurar no arquivo .env o path da API API_PATH = config('API_PATH')**

-----------------------

## Executando o build do projeto flutter

**Sugerimos utilizar o ambiente virtual para executar o build do projeto flutter, o uso em container não foi testado.**

```console
python manage.py flutter
```
