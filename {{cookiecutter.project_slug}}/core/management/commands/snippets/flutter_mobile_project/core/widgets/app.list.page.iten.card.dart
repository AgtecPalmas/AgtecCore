import 'package:flutter/material.dart';

import '../../constants/app.colors.dart';
import '../../constants/app.sizes.dart';

class AppListPageItenCard<T> extends StatefulWidget {
  // Item genérico para o card
  final T item;
  // Função para ser chamada quando clicar no ícone de editar
  final Function()? onEdit;
  // Função para ser chamada quando clicar no ícone de visualizar
  final Function()? onView;
  // Função para ser chamada quando clicar no ícone de deletar
  final Function()? onDelete;

  const AppListPageItenCard({super.key, required this.item, this.onEdit, this.onView, this.onDelete});

  @override
  State<AppListPageItenCard> createState() => _AppListPageItenCardState();
}

class _AppListPageItenCardState extends State<AppListPageItenCard> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      height: 125,
      decoration: BoxDecoration(
        color: AppColors.listViewPageContainerItenBackground,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(AppSizeMarginPadding.cardRadiusDefault),
          bottomLeft: Radius.circular(AppSizeMarginPadding.cardRadiusDefault),
        ),
        border: Border.all(color: AppColors.gray858080),
      ),
      padding: const EdgeInsets.only(
        left: AppSizeMarginPadding.marginDefaultTRBL,
        top: AppSizeMarginPadding.marginDefaultTRBL,
      ),
      margin: const EdgeInsets.only(
        left: AppSizeMarginPadding.marginDefaultTRBL,
        right: 0,
        bottom: AppSizeMarginPadding.marginDefaultTRBL,
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              IconButton(
                onPressed: widget.onEdit,
                icon: Icon(Icons.edit, color: AppColors.listViewPageContainerChildrensForeground),
              ),
              IconButton(
                onPressed: widget.onView,
                icon: Icon(Icons.remove_red_eye, color: AppColors.listViewPageContainerChildrensForeground),
              ),
            ],
          ),
          SizedBox(width: AppSizeMarginPadding.marginDefaultTRBL),
          Expanded(
            child: Text(
              widget.item.toString(),
              style: TextStyle(color: AppColors.listViewPageContainerChildrensForeground),
            ),
          ),
          SizedBox(
            height: 140,
            child: Align(
              alignment: Alignment.bottomRight,
              child: IconButton(
                onPressed: widget.onDelete,
                icon: Icon(Icons.delete_outline_outlined, color: AppColors.listViewPageContainerChildrensDeleteIcon),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
