# Projeto Flutter Web

## Descrição

Projeto gerado por meio do build-flutter-web do AgtecCore, seguindo os mesmos
conceitos do build-flutter. 

-----

## Dados do projeto
### Flutter 3.29.3
### Dart 3.7.0

----- 

## Pacotes de ícones 

No projeto o site utilizado como fonte para os ícones é o [HeroIcons](https://heroicons.com/), onde os ícones são baixados em SVG e convertidos para PNG. Mas caso utilizar outro site trazemos como
sugestão:

- [Font Awesome](https://fontawesome.com/)
- [Icons8](https://icons8.com/icons)
- [Flaticon](https://www.flaticon.com/)
- [IconFinder](https://www.iconfinder.com/)
- [IconScout](https://iconscout.com/)
- [Iconmonstr](https://iconmonstr.com/)

-----

## Pacotes padrões 

- [BrasilFields](https://pub.dev/packages/brasil_fields)
- [Bloc](https://pub.dev/packages/bloc)
- [Dio](https://pub.dev/packages/dio)
- [Either](https://pub.dev/packages/either_dart)
- [Equatable](https://pub.dev/packages/equatable)
- [FlutterBloc](https://pub.dev/packages/flutter_bloc)
- [GoRouter](https://pub.dev/packages/go_router)
- [GetIT](https://pub.dev/packages/get_it)
- [ImagePicker](https://pub.dev/packages/image_picker)
- [Logger](https://pub.dev/packages/logger)
- [PrettyDioLogger](https://pub.dev/packages/pretty_dio_logger)
- [SembastWeb](https://pub.dev/packages/sembast_web)
- [SecureStorage](https://pub.dev/packages/flutter_secure_storage)
- [ValidatorLess](https://pub.dev/packages/validatorless)

------

## Estrutura do projeto

```bash
flutter_web/
    ├── assets
    ├── build
    ├── lib
    │   ├── apps
    │   ├── constants
    │   ├── core
    │       ├── dio
    │       ├── exceptions
    │       ├── extensions
    │       ├── guards
    │       ├── interfaces
    │       ├── secure
    │       ├── styles
    │       ├── widgets
    │   ├── main.dart
    ├── tests
    ├── web
    ├── analysis_options.yaml
    ├── pubspec.yaml
    ├── README.md
```

----- 

## Exemplo de uso dos componentes padrões

### AppTableActions
Componente para renderizar ações em tabelas.
```dart
AppTableColumnActions(
    title: 'Ações',
    width: const FixedColumnWidth(120),
    dataSelector: (SettingsModels item) => Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
        InkWell(
        onTap: () {},
        child: Image.asset(
            'assets/icons/edit.png',
            width: 20, height: 20,
            color: AppColors.editButtonIcon,
        ),
        ),
        InkWell(
        onTap: () {},
        child: Image.asset(
            'assets/icons/disabled.png',
            width: 20, height: 20,
            color: AppColors.disabledButtonIcon,
        ),
        ),
        InkWell(
        onTap: () {},
        child: Image.asset(
            'assets/icons/delete.png',
            width: 20, height: 20,
            color: AppColors.deleteButtonIcon,
        ),
        ),
    ],
    ),
),
```

