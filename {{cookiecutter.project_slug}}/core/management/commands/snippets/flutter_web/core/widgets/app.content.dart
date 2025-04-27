import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/extensions/open.modal.form.dart';
import '/core/styles/app.button.style.dart';
import '/core/styles/app.formfield.style.dart';
import '/core/styles/app.text.style.dart';
import '/core/widgets/app.card.dart';
import '/core/widgets/app.header.content.page.dart';
import '/core/widgets/app.inputformfield.dart';
import '/core/widgets/app.modal.dart';
import '/core/widgets/app.table.dart';

class AppContentContainer extends StatelessWidget {
  const AppContentContainer({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(
        top: AppSizeMarginPadding.marginDefaultTRBL,
        left: AppSizeMarginPadding.marginMenuItemContentH,
        right: AppSizeMarginPadding.marginDefaultTRBL,
      ),
      decoration: const BoxDecoration(
        color: AppColors.transparent,
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const AppHeaderPage(title: 'Dashboard'),
          AppCard(
            cardTitle: 'Título do Card',
            cardContent: Row(
              children: [
                const Icon(Icons.access_alarm),
                const SizedBox(width: 8),
                const Text('Conteúdo do Card'),
                const SizedBox(width: 8),
                const Spacer(),
                ElevatedButton(onPressed: () {}, style: AppButtonPrimaryStyle.style(), child: const Text('Botão')),
                const SizedBox(width: 8),
                OutlinedButton(
                    onPressed: () {}, style: AppButtonOutlinedStyle.style(), child: const Text('Botão Outline')),
              ],
            ),
          ),
          AppCard(
            cardTitle: 'Título do Card',
            cardContent: Row(
              children: [
                const Icon(Icons.access_alarm),
                const SizedBox(width: 8),
                const Text('Conteúdo do Card'),
                const SizedBox(width: 8),
                const Spacer(),
                ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      context.openModalWidgetCenter(
                        const AppModal(
                          title: 'Adicionar Produto',
                          child: Text('Modal Centralizado'),
                        ),
                      ),
                    );
                  },
                  style: AppButtonPrimaryStyle.style(),
                  child: const Text('Abrir Modal Central'),
                ),
                const SizedBox(width: 8),
                OutlinedButton(
                  onPressed: () {},
                  style: AppButtonOutlinedStyle.style(),
                  child: const Text('Botão Outline'),
                ),
              ],
            ),
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: AppCard(
                  cardTitle: 'Últimas Atividades',
                  cardContent: Row(
                    children: [
                      const Icon(Icons.access_alarm),
                      const SizedBox(width: 8),
                      const Text('Conteúdo do Card'),
                      const SizedBox(width: 8),
                      const Spacer(),
                      ElevatedButton(
                          onPressed: () {}, style: AppButtonPrimaryStyle.style(), child: const Text('Botão')),
                      const SizedBox(width: 8),
                      OutlinedButton(
                          onPressed: () {}, style: AppButtonOutlinedStyle.style(), child: const Text('Botão Outline')),
                    ],
                  ),
                ),
              ),
              const SizedBox(
                width: AppSizeMarginPadding.spaceDefaultH,
              ),
              Expanded(
                child: AppCard(
                  cardTitle: 'Últimas Atividades',
                  cardContent: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(
                        width: double.infinity,
                        child: Table(
                          defaultVerticalAlignment: TableCellVerticalAlignment.middle,
                          columnWidths: const {
                            0: FixedColumnWidth(100),
                            1: FixedColumnWidth(100),
                            2: FixedColumnWidth(100),
                          },
                          children: [
                            TableRow(
                              children: [
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
                              ],
                            ),
                            TableRow(
                              children: [
                                Text('Item 1', style: AppTableItemStyle.style()),
                                Text('Item 2', style: AppTableItemStyle.style()),
                                Text('Item 3', style: AppTableItemStyle.style()),
                              ],
                            ),
                            const TableRow(
                              children: [
                                AppTableDivider(),
                                AppTableDivider(),
                                AppTableDivider(),
                              ],
                            ),
                            TableRow(
                              children: [
                                Text('Item 56', style: AppTableItemStyle.style()),
                                Text('Item 678', style: AppTableItemStyle.style()),
                                Text('Item 87878', style: AppTableItemStyle.style()),
                              ],
                            ),
                          ],
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ],
          ),
          AppCard(
            cardTitle: 'Formulários de Cadastro',
            cardContent: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: AppWidgetContainerInputFormField(
                    labelText: 'Nome',
                    textFormField: TextFormField(
                      decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu nome'),
                    ),
                  ),
                ),
                const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
                Expanded(
                  child: AppWidgetContainerInputFormField(
                    labelText: 'Email',
                    textFormField: TextFormField(
                      decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu e-mail'),
                    ),
                  ),
                ),
                const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
                Expanded(
                  child: AppWidgetContainerInputFormField(
                    labelText: 'Telefone',
                    textFormField: TextFormField(
                      decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu telefone'),
                    ),
                  ),
                ),
                const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
                Expanded(
                  child: AppWidgetContainerInputFormField(
                    labelText: 'WhatsApp',
                    textFormField: TextFormField(
                      decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite seu WhatsApp'),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
