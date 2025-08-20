import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.card.style.dart';
import '/core/styles/app.text.style.dart';
import '/core/widgets/app.menuitem.dart';

import '../../constants/app.colors.dart';

class AppMenuToolbar extends StatefulWidget {
  const AppMenuToolbar({super.key, required this.currentPath});
  final String currentPath;

  @override
  State<AppMenuToolbar> createState() => _AppMenuToolbarState();
}

class _AppMenuToolbarState extends State<AppMenuToolbar> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: AppSizeMarginPadding.menuW,
      margin: const EdgeInsets.only(
        top: AppSizeMarginPadding.marginDefaultTRBL,
        left: AppSizeMarginPadding.marginMenuItemL,
        right: AppSizeMarginPadding.marginMenuItemR,
      ),
      padding: const EdgeInsets.all(AppSizeMarginPadding.paddingDefaultTRBL),
      decoration: BoxDecoration(
        color: AppColors.menuBackground,
        borderRadius: const BorderRadius.all(Radius.circular(
          AppSizeMarginPadding.cardRadiusDefault,
        )),
        border: Border(
          left: AppCardStyle.style(), // Use the style method from AppCardStyle
          right: AppCardStyle.style(),
          top: AppCardStyle.style(),
          bottom: AppCardStyle.style(),
        ),
      ),
      child: Column(
        children: [
          _buildHeaderMenuItem(),
          const SizedBox(
            height: AppSizeMarginPadding.marginDefaultTRBL,
          ),
          $AppsMenuItem$
          const Spacer(),
          _buildConfigMenuItem(),
        ],
      ),
    );
  }

  /// Método para construir o cabeçalho do menu
  Widget _buildHeaderMenuItem() {
    return InkWell(
      onTap: () {
        context.go('/dashboard');
      },
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.asset(
            'assets/icons/icon.png',
            width: 34,
            height: 34,
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              'Connecta Federação',
              style: AppTitleMenuStyle.style(),
            ),
          ),
        ],
      ),
    );
  }

  /// Método para construir o iten de configuração do menu
  /// que deverá ficar alinhado à parte inferior do menu
  /// com o ícone de configuração
  ///
  Widget _buildConfigMenuItem() {
    return AppMenuItem(
        title: 'Configurações',
        icon: 'settings.png',
        isSelected: widget.currentPath == 'settings',
        onTap: () {
          context.go('/settings');
        });
  }
}
