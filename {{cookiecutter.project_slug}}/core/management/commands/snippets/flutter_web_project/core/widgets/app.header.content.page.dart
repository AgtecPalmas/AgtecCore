// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

class AppHeaderPage extends StatefulWidget {
  final String title;
  final bool searchEnabled;
  const AppHeaderPage({
    super.key,
    required this.title,
    this.searchEnabled = false,
  });

  @override
  State<AppHeaderPage> createState() => _AppHeaderPageState();
}

class _AppHeaderPageState extends State<AppHeaderPage> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Text(
            widget.title,
            style: AppTextTitlePageStyle.style(),
          ),
          Visibility(
            visible: widget.searchEnabled,
            child: _buildSearch(),
          ),
          const Spacer(),
          Text('Olá Usuário', style: AppUserNameStyle.style()),
          const SizedBox(
            width: AppSizeMarginPadding.userNameToAvatarSpaceH,
          ),
          const SizedBox(
            width: AppSizeMarginPadding.avatarHeaderWH,
            child: CircleAvatar(
              radius: AppSizeMarginPadding.iconMenuDefaultWH,
              backgroundImage: AssetImage('assets/images/avatar.png'),
            ),
          ),
        ],
      ),
    );
  }

  /// Método para construir o componente de pesquisa
  ///
  /// @returns Widget
  ///
  Widget _buildSearch() {
    return Expanded(
      child: Container(
        constraints: const BoxConstraints(
          maxHeight: AppSizeMarginPadding.searchHeaderHeight,
        ),
        margin: const EdgeInsets.only(
          left: AppSizeMarginPadding.marginSearchHeaderL,
          right: AppSizeMarginPadding.marginSearchHeaderR,
        ),
        decoration: BoxDecoration(
          color: AppColors.searchFieldBackground,
          borderRadius: BorderRadius.circular(AppSizeMarginPadding.searchFieldRadius),
          border: Border.all(
            color: AppColors.textFormFieldBorder,
            width: AppSizeMarginPadding.inputTextFormFieldBorderSize,
          ),
        ),
        child: const TextField(
          textAlignVertical: TextAlignVertical.center,
          decoration: InputDecoration(
            hintText: 'Pesquisar',
            border: InputBorder.none,
            prefixIcon: Icon(
              Icons.search,
              color: AppColors.searchFieldIcon,
            ),
          ),
        ),
      ),
    );
  }
}
