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

### AppTableColumn
Componente para renderizar colunas de tabelas.
```dart
AppTableColumnString(
    title: '...',
    dataSelector: (XPTOModel item) => item.xpto,
),
```

### AppDropdownMenu
```dart
return AppContainerDropdownMenu(
      title: 'Tipo de Evento',
      dropdownMenu: DropdownMenu<String>(
        controller: _eventoFormTipo,
        requestFocusOnTap: true,
        enableFilter: true,
        menuHeight: 300,
        width: constraints.maxWidth * 0.5,
        menuStyle: DropdownMenuStyle.style(),
        hintText: 'Selecione o tipo do evento',
        textStyle: DropdownMenuTextStyle.style(),
        inputDecorationTheme: DropdownInputDecorationTheme.style(),
        dropdownMenuEntries:
            widget.tipoEventoList.map((e) => DropdownMenuEntry<String>(value: e.id, label: e.nome)).toList(),
        onSelected: (value) {
          setState(() {
            // Encontra o item selecionado na lista de tipos de eventos
            final selectedTipoEvento = widget.tipoEventoList.firstWhere(
              (item) => item.id == value,
              orElse: () => TipoEventoModel(),
            );
            // Atualiza o ID do tipo de evento selecionado
            tipoEventoID = selectedTipoEvento.id;
            // Atualiza o campo de texto do tipo de evento com o nome do tipo selecionado
            _eventoFormTipo.text = selectedTipoEvento.nome;
          });
        },
      ),
    );
```

### AppSwitchFormField
```dart
AppWidgetSwitchFormField(
    labelText: 'Presencial ${eventoPresencial ? 'Sim' : 'Não'}',
    value: eventoPresencial,
    onChanged: (value) {
        setState(() {
        eventoPresencial = value;
        });
    },
    ),
)
```

### AppTextFormField
```dart
AppWidgetContainerInputFormField(
    labelText: 'Local',
    textFormField: TextFormField(
        controller: _eventoFormLocals,
        onTapOutside: (_) => FocusScope.of(context).unfocus(),
        validator: Validatorless.multiple([Validatorless.required('Campo obrigatório')]),
        decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite o Local'),
    ),
)
```
