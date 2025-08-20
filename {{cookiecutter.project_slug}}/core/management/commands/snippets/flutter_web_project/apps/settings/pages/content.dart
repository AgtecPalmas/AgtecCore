import 'package:flutter/material.dart';
import '/apps/settings/models/settings.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/app.logger.dart';
import '/core/extensions/open.modal.form.dart';
import '/core/styles/app.button.style.dart';
import '/core/styles/app.formfield.style.dart';
import '/core/widgets/app.card.dart';
import '/core/widgets/app.form.modal.dart';
import '/core/widgets/app.header.content.page.dart';
import '/core/widgets/app.inputformfield.dart';
import '/core/widgets/app.table.dart';

class ContentSettingPage extends StatefulWidget {
  const ContentSettingPage({super.key});

  @override
  State<ContentSettingPage> createState() => _ContentSettingPageState();
}

class _ContentSettingPageState extends State<ContentSettingPage> {
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
                title: 'Consigurações',
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
                  cardContent: buildTable(),
                ),
              )
            ],
          ),
        ),
      );
    });
  }

  /// Método de exemplo para construir uma AppTable passando dados genéricos para ela
  ///
  Widget buildTable() {
    // TODO Verificar como adicionar o SingleChildScrollView
    // Criando 12 itens de exemplo
    final items = List.generate(
      12,
      (index) => SettingsModels(
        id: index.toString(),
        name: 'Item $index',
        description: 'Description for item $index',
      ),
    );
    return AppTable<SettingsModels>(
      items: items,
      columns: [
        AppTableColumnActions(
          title: 'Ações',
          width: const FixedColumnWidth(120),
          dataSelector: (SettingsModels item) => Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              InkWell(
                onTap: () {
                  /// Chamando o FormModal passando como parâmetro o widget
                  /// o item que foi clicado
                  Navigator.of(context).push(
                    context.openModalWindow(
                      AppFormModal(
                        title: 'Editar Produto ${item.name}',
                        child: _buildFormExample(),
                      ),
                    ),
                  );
                },
                child: Image.asset(
                  'assets/icons/edit.png',
                  width: 20,
                  height: 20,
                  color: AppColors.editButtonIcon,
                ),
              ),
              InkWell(
                onTap: () {
                  AppLogger().info('Ativando/desativando item ${item.name}');
                },
                child: Image.asset(
                  'assets/icons/disabled.png',
                  width: 20,
                  height: 20,
                  color: AppColors.disabledButtonIcon,
                ),
              ),
              InkWell(
                onTap: () {
                  AppLogger().info('Deletando item ${item.name}');
                },
                child: Image.asset(
                  'assets/icons/delete.png',
                  width: 20,
                  height: 20,
                  color: AppColors.deleteButtonIcon,
                ),
              ),
            ],
          ),
        ),
        AppTableColumnString(
          title: 'Nome',
          dataSelector: (SettingsModels item) => item.name ?? '',
        ),
        AppTableColumnString(
          title: 'Descrição',
          dataSelector: (SettingsModels item) => item.description ?? '',
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
