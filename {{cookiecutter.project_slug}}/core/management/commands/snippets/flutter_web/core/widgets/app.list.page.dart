import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/extensions/open.modal.form.dart';
import '/core/styles/app.button.style.dart';
import '/core/styles/app.formfield.style.dart';
import '/core/styles/app.text.style.dart';
import '/core/widgets/app.card.dart';
import '/core/widgets/app.form.modal.dart';
import '/core/widgets/app.header.content.page.dart';
import '/core/widgets/app.inputformfield.dart';
import '/core/widgets/app.table.dart';

class AppListViewPage extends StatefulWidget {
  const AppListViewPage({super.key});

  @override
  State<AppListViewPage> createState() => _AppListViewPageState();
}

class _AppListViewPageState extends State<AppListViewPage> {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (BuildContext contextLB, BoxConstraints constraints) {
      return Container(
        margin: const EdgeInsets.only(
          top: AppSizeMarginPadding.marginDefaultTRBL,
          left: AppSizeMarginPadding.marginMenuItemContentH,
          right: AppSizeMarginPadding.marginDefaultTRBL,
        ),
        decoration: const BoxDecoration(
          color: AppColors.transparent,
        ),
        child: Expanded(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const AppHeaderPage(
                title: 'Listagem de Produtos',
                searchEnabled: true,
              ),
              Align(
                alignment: Alignment.centerRight,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      context.openModalWindow(
                        AppFormModal(
                          title: 'Adicionar Produto',
                          child: _buildFormExample(),
                        ),
                      ),
                    );
                  },
                  style: AppButtonPrimaryStyle.style(),
                  child: const Text('Adicionar'),
                ),
              ),
              Expanded(
                child: AppCard(
                  cardTitle: '',
                  cardContent: Column(
                    children: [
                      _buildTable(),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      );
    });
  }

  /// Método para retornar a tabela que conterá os itens
  /// que será preenchida por maio de genérics
  ///
  Widget _buildTable() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
        horizontal: AppSizeMarginPadding.paddingTableH,
      ),
      child: Table(
        defaultVerticalAlignment: TableCellVerticalAlignment.middle,
        columnWidths: const {
          0: FixedColumnWidth(50),
          1: FixedColumnWidth(100),
          2: FixedColumnWidth(100),
          3: FixedColumnWidth(100)
        },
        children: [
          TableRow(
            children: [
              Text('Ações', style: AppTableHeaderStyle.style()),
              Text('Coluna 1', style: AppTableHeaderStyle.style()),
              Text('Coluna 2', style: AppTableHeaderStyle.style()),
              Text('Coluna 3', style: AppTableHeaderStyle.style()),
            ],
          ),
          // Adicionando espaço entre o cabeçalho e os itens
          const TableRow(
            children: [
              SizedBox(height: AppSizeMarginPadding.spaceTableHeadToItem),
              SizedBox(height: AppSizeMarginPadding.spaceTableHeadToItem),
              SizedBox(height: AppSizeMarginPadding.spaceTableHeadToItem),
              SizedBox(height: AppSizeMarginPadding.spaceTableHeadToItem),
            ],
          ),
          TableRow(
            children: [
              _buildActions('itemId'),
              Text('Item 2', style: AppTableItemStyle.style()),
              Text('Item 3', style: AppTableItemStyle.style()),
              Text('Item 3', style: AppTableItemStyle.style()),
            ],
          ),
          const TableRow(
            children: [
              AppTableDivider(),
              AppTableDivider(),
              AppTableDivider(),
              AppTableDivider(),
            ],
          ),
          TableRow(
            children: [
              _buildActions('itemId', isEnabled: false),
              Text('Item 678', style: AppTableItemStyle.disabled()),
              Text('Item 87878', style: AppTableItemStyle.disabled()),
              Text('Item 87878', style: AppTableItemStyle.disabled()),
            ],
          ),
          const TableRow(
            children: [
              AppTableDivider(),
              AppTableDivider(),
              AppTableDivider(),
              AppTableDivider(),
            ],
          ),
          TableRow(
            children: [
              _buildActions('itemId'),
              Text('Item 678', style: AppTableItemStyle.style()),
              Text('Item 87878', style: AppTableItemStyle.style()),
              Text('Item 87878', style: AppTableItemStyle.style()),
            ],
          ),
        ],
      ),
    );
  }

  /// Método para retornar as ações do item
  ///
  /// [Params]
  ///  @required String itemId
  ///
  /// [Returns]
  /// Widget
  ///
  ///
  Widget _buildActions(String itemId, {bool isEnabled = true}) {
    return Row(
      children: [
        InkWell(
          onTap: () {},
          child: Container(
            width: AppSizeMarginPadding.iconMenuDefaultWH,
            height: AppSizeMarginPadding.iconMenuDefaultWH,
            decoration: const BoxDecoration(
              color: AppColors.menuBackground,
              borderRadius: BorderRadius.all(
                Radius.circular(AppSizeMarginPadding.iconMenuDefaultWH),
              ),
            ),
            child: Image.asset(
              'assets/icons/edit.png',
              width: AppSizeMarginPadding.iconMenuDefaultWH,
              height: AppSizeMarginPadding.iconMenuDefaultWH,
              color: AppColors.editButtonIcon,
            ),
          ),
        ),
        InkWell(
          onTap: () {},
          child: Container(
            width: AppSizeMarginPadding.iconMenuDefaultWH,
            height: AppSizeMarginPadding.iconMenuDefaultWH,
            decoration: const BoxDecoration(
              color: AppColors.menuBackground,
              borderRadius: BorderRadius.all(
                Radius.circular(AppSizeMarginPadding.iconMenuDefaultWH),
              ),
            ),
            child: Image.asset(
              'assets/icons/delete.png',
              width: AppSizeMarginPadding.iconMenuDefaultWH,
              height: AppSizeMarginPadding.iconMenuDefaultWH,
              color: AppColors.deleteButtonIcon,
            ),
          ),
        ),
        Visibility(
          visible: isEnabled,
          child: InkWell(
            onTap: () {},
            child: Container(
              width: AppSizeMarginPadding.iconMenuDefaultWH,
              height: AppSizeMarginPadding.iconMenuDefaultWH,
              decoration: const BoxDecoration(
                color: AppColors.menuBackground,
                borderRadius: BorderRadius.all(
                  Radius.circular(AppSizeMarginPadding.iconMenuDefaultWH),
                ),
              ),
              child: Image.asset(
                'assets/icons/enabled.png',
                width: AppSizeMarginPadding.iconMenuDefaultWH,
                height: AppSizeMarginPadding.iconMenuDefaultWH,
                color: AppColors.enabledButtonIcon,
              ),
            ),
          ),
        ),
        Visibility(
          visible: !isEnabled,
          child: InkWell(
            onTap: () {},
            child: Container(
              width: AppSizeMarginPadding.iconMenuDefaultWH,
              height: AppSizeMarginPadding.iconMenuDefaultWH,
              decoration: const BoxDecoration(
                color: AppColors.menuBackground,
                borderRadius: BorderRadius.all(
                  Radius.circular(AppSizeMarginPadding.iconMenuDefaultWH),
                ),
              ),
              child: Image.asset(
                'assets/icons/disabled.png',
                width: AppSizeMarginPadding.iconMenuDefaultWH,
                height: AppSizeMarginPadding.iconMenuDefaultWH,
                color: AppColors.disabledButtonIcon,
              ),
            ),
          ),
        ),
      ],
    );
  }

  /// Método para renderizar um form para ser
  /// aberto no modal, caso o usuário clique no botão
  /// Adicionar
  ///
  Widget _buildFormExample() {
    return Expanded(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Row(
            children: [
              Expanded(
                child: AppWidgetContainerInputFormField(
                  labelText: 'Produto',
                  textFormField: TextFormField(
                    decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu WhatsApp'),
                  ),
                ),
              ),
              Expanded(
                child: AppWidgetContainerInputFormField(
                  labelText: 'Validade',
                  textFormField: TextFormField(
                    decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu WhatsApp'),
                  ),
                ),
              ),
            ],
          ),
          AppWidgetContainerInputFormField(
            labelText: 'Descrição',
            textFormField: TextFormField(
              maxLines: 5,
              decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu WhatsApp'),
            ),
          ),
          const Spacer(),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              ElevatedButton(onPressed: () {}, style: AppButtonPrimaryStyle.style(), child: const Text('Salvar')),
              const SizedBox(width: 8),
              OutlinedButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  style: AppButtonOutlinedStyle.style(),
                  child: const Text('Cancelar')),
            ],
          ),
        ],
      ),
    );
  }
}
