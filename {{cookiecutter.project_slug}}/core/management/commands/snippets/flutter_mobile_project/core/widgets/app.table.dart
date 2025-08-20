import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

/// Class para renderizar a tabela recebendo os dados por meio de
/// generics
///
///

class AppTable<T> extends StatelessWidget {
  const AppTable({super.key, required this.items, required this.columns, this.maxWidth = 1280});

  final List<T> items;
  final List<AppTableColumn<T>> columns;
  final double maxWidth;

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.topLeft,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: ConstrainedBox(
          constraints: BoxConstraints(
            maxWidth: maxWidth,
          ),
          child: Material(
            color: Colors.white,
            child: Table(
              columnWidths: Map.fromEntries(
                columns.where((c) => c.width != null).map(
                      (c) => MapEntry(columns.indexOf(c), c.width!),
                    ),
              ),
              children: [
                TableRow(
                  children: [
                    for (final c in columns)
                      TableCell(
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Text(
                            c.title,
                            style: AppTableHeaderStyle.style(),
                          ),
                        ),
                      ),
                  ],
                ),
                buildTableRowSpaceBetweenHeaderAndItems(columns.length),

                /// Percorrendo item a item
                for (final i in items) buildTableRowItenAndSeparator(i, columns),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Método para criar as linhas com os itens
/// e um separador entre eles
///
/// Params:
///   [int] - Tamanho da lista de colunas
///
/// Returns:
///   [TableRow] - Retorna uma linha com o tamanho da lista de colunas
///
TableRow buildTableRowItenAndSeparator(iten, List<AppTableColumn> columns) {
  return TableRow(
    children: [
      for (final c in columns)
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              height: AppSizeMarginPadding.tableRowHeight,
              child: c.builder(iten),
            ),
            const AppTableDivider(),
          ],
        )
    ],
  );
}

/// Método para criar as colunas de espaçamento
/// entre o head da table e os itens
///
/// Params:
///  [int] - Tamanho da lista de colunas
///
/// Returns:
///   [TableRow] - Retorna uma linha com o tamanho da lista de colunas
///
TableRow buildTableRowSpaceBetweenHeaderAndItems(int columnsLength) {
  return TableRow(
    children: [
      for (final _ in List.generate(columnsLength, (index) => index))
        const SizedBox(height: AppSizeMarginPadding.spaceTableHeadToItem)
    ],
  );
}

/// Classe para renderizar o componente de separação das linhas
/// da tabela
///
class AppTableDivider extends StatelessWidget {
  const AppTableDivider({super.key});

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.symmetric(
        vertical: AppSizeMarginPadding.spaceTableSeparateLinesItem,
      ),
      child: Divider(
        color: AppColors.separatorTableLine,
        height: AppSizeMarginPadding.tableSeparatorHeight,
      ),
    );
  }
}

///
/// [======================================================]
/// Classes para renderização das colunas da tabela
/// [======================================================]
///

/// Classe abstrata para renderização das colunas da tabela
///
abstract class AppTableColumn<T> {
  AppTableColumn({required this.title, this.width});

  final String title;
  final TableColumnWidth? width;

  Widget builder(T item);
}

/// Classe para renderização de colunas do tipo inteiro
///
class AppTableColumnString<T> extends AppTableColumn<T> {
  AppTableColumnString({
    required super.title,
    required this.dataSelector,
    super.width,
  });

  final String Function(T) dataSelector;

  @override
  Widget builder(T item) {
    return Text(dataSelector(item), style: AppTableItemStyle.style());
  }
}

/// Classe para renderização de colunas do tipo monetário
///
class AppTableColumnMoney<T> extends AppTableColumn<T> {
  AppTableColumnMoney({
    required super.title,
    required this.dataSelector,
    super.width,
  });

  final int Function(T) dataSelector;

  @override
  Widget builder(T item) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Text(NumberFormat.simpleCurrency(locale: 'pt-BR').format(dataSelector(item) / 100)),
    );
  }
}

/// Classe para renderização de colunas que recebem widgets
/// como filhos
///
class AppTableColumnWidget<T> extends AppTableColumn<T> {
  AppTableColumnWidget({
    required super.title,
    required this.dataSelector,
    super.width,
  });

  final Widget Function(T) dataSelector;

  @override
  Widget builder(T item) {
    return dataSelector(item);
  }
}

/// Classe para renderização de colunas que recebem widgets
/// como filhos
///
class AppTableColumnActions<T> extends AppTableColumn<T> {
  AppTableColumnActions({
    required super.title,
    required this.dataSelector,
    super.width,
  });

  final Widget Function(T) dataSelector;

  @override
  Widget builder(T item) {
    return Padding(
      padding: const EdgeInsets.only(
        right: AppSizeMarginPadding.paddingTableColumnActionR,
      ),
      child: dataSelector(item),
    );
  }
}

/// Classe para renderização de colunas que recebem imagens
///
class AppTableColumnImage<T> extends AppTableColumn<T> {
  AppTableColumnImage({
    required super.title,
    required this.dataSelector,
    super.width,
  });

  final String Function(T) dataSelector;

  @override
  Widget builder(T item) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Image.network(dataSelector(item), fit: BoxFit.cover, width: 100),
    );
  }
}
