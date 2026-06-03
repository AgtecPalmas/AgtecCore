import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:validatorless/validatorless.dart';

import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/extensions/open.modal.form.dart';
import '/core/styles/app.button.style.dart';
import '/core/styles/app.formfield.style.dart';
import '/core/widgets/app.card.dart';
import '/core/widgets/app.header.content.page.dart';
import '/core/widgets/app.inputformfield.dart';
import '/core/widgets/app.modal.dart';
import '../../../core/app.logger.dart';
import '../../../core/app.mixins.dart';
import '../controllers/dashboard.dart';

class DashboardContent extends StatefulWidget {
  const DashboardContent({super.key});

  @override
  State<DashboardContent> createState() => _DashboardContentState();
}

class _DashboardContentState extends State<DashboardContent> with MessagesMixin {
  late final DashboardController _dashboardController;

  final _formKey = GlobalKey<FormState>();
  final inputTextControllerFilterFiliado = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadData();
    });
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (BuildContext contextLB, BoxConstraints constraints) {
        return Container(
          margin: const EdgeInsets.only(
            top: AppSizeMarginPadding.marginDefaultTRBL,
            left: AppSizeMarginPadding.marginMenuItemContentH,
            right: AppSizeMarginPadding.marginDefaultTRBL,
          ),
          decoration: const BoxDecoration(color: AppColors.transparent),
          child: CustomScrollView(
            slivers: [
              SliverToBoxAdapter(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.start,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const AppHeaderPage(title: 'Início'),
                    _buildDashBoardCardAcoes(context),
                    _buildDashBoardCardEvolucaoFinanceira(context),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(flex: 2, child: _buildDashBoardCardPesquisarFiliados(context)),
                        const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
                        Expanded(child: _buildDashBoardCardListaAniversariantes(context)),
                      ],
                    ),
                    _buildDashBoardFormCadastrarNovoFiliado(),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  ///
  /// Método para retornar o card de formulário de cadastro de novo filiado
  ///
  Widget _buildDashBoardFormCadastrarNovoFiliado() {
    return AppCard(
      cardTitle: 'Cadastrar novo filiado',
      cardContent: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Row(
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
          ElevatedButton(onPressed: () {}, style: AppButtonPrimaryStyle.style(), child: const Text('Salvar')),
        ],
      ),
    );
  }

  ///
  /// Método para retornar o card com botões de ação
  ///
  Widget _buildDashBoardCardAcoes(BuildContext context) {
    return AppCard(
      cardTitle: 'Ações Rápidas',
      cardContent: Wrap(
        children: [
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).push(
                context.openModalWidgetCenter(
                  const AppModal(title: 'Adicionar Produto', child: Text('Adicionando novo produto')),
                ),
              );
            },
            style: AppButtonPrimaryStyle.style(),
            child: const Text('Abrir Modal Central'),
          ),
          const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).push(
                context.openModalWidgetCenter(
                  const AppModal(title: 'Enviar Mensagem à filiado.', child: Text('Enviando mensagem...')),
                ),
              );
            },
            style: AppButtonPrimaryStyle.style(),
            child: const Text('Enviar Mensagem à filiado'),
          ),
          const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).push(
                context.openModalWidgetCenter(
                  const AppModal(title: 'Bloquear acesso', child: Text('Bloquear acesso ao sistema')),
                ),
              );
            },
            style: AppButtonPrimaryStyle.style(),
            child: const Text('Bloquear acesso'),
          ),
          const SizedBox(width: AppSizeMarginPadding.spaceDefaultH),
        ],
      ),
    );
  }

  ///
  /// Método para retornar o card de evolução financeira
  ///
  Widget _buildDashBoardCardEvolucaoFinanceira(BuildContext context) {
    return AppCard(
      cardTitle: 'Evolução Financeira',
      cardContent: Column(
        children: [
          Row(
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
                      const AppModal(title: 'Adicionar Produto', child: Text('Modal Centralizado')),
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
        ],
      ),
    );
  }

  ///
  /// Método para retornar o card de pesquisa dos filiados
  ///
  Widget _buildDashBoardCardPesquisarFiliados(BuildContext context) {
    return AppCard(
      cardTitle: 'Pesquisar filiados',
      cardContent: Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            AppWidgetContainerInputFormField(
              labelText: 'Nome do filiado',
              textFormField: TextFormField(
                controller: inputTextControllerFilterFiliado,
                decoration: AppInputTextFormFieldStyle.style(hintText: 'Digite o nome do filiado'),
                validator: Validatorless.multiple([
                  Validatorless.required('O nome do filiado é obrigatório.'),
                  Validatorless.min(3, 'O nome do filiado deve ter pelo menos 3 caracteres.'),
                ]),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                if (_formKey.currentState?.validate() ?? false) {}
              },
              style: AppButtonPrimaryStyle.style(),
              child: const Text('Pesquisar'),
            ),
          ],
        ),
      ),
    );
  }

  ///
  /// Método para retornar o card de listagem de aniversariantes do mês
  ///
  Widget _buildDashBoardCardListaAniversariantes(BuildContext context) {
    return AppCard(
      cardTitle: 'Aniversariantes do mês',
      cardContent: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [SizedBox(width: double.infinity, child: SizedBox.shrink())],
      ),
    );
  }

  ///
  /// Método para carregar os dados iniciais
  /// o método deve implementar o controle de resquisição de dados
  ///
  Future<void> _loadData() async {
    try {
      _dashboardController = context.read<DashboardController>();
      await Future.wait([]);
    } catch (error, stackTrace) {
      AppLogger().erro('#controller_layer', error, stackTrace);
    }
  }
}
