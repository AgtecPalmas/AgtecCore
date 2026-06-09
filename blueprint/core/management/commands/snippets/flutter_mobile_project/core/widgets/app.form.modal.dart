import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

class AppFormModal extends StatefulWidget {
  final Widget child;
  final String title;

  const AppFormModal({super.key, required this.child, required this.title});

  @override
  State<AppFormModal> createState() => _AppFormModalState();
}

class _AppFormModalState extends State<AppFormModal> {
  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.modalFormBackground,
      child: Container(
        width: double.infinity,
        height: double.infinity,
        margin: const EdgeInsets.symmetric(
          vertical: AppSizeMarginPadding.marginModalFormBottom,
        ),
        padding: const EdgeInsets.all(0),
        color: AppColors.transparent,
        child: Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            _buildModalBackground(),
            Container(
              width: MediaQuery.sizeOf(context).width * .70,
              height: MediaQuery.sizeOf(context).height,
              padding: const EdgeInsets.symmetric(
                horizontal: AppSizeMarginPadding.paddingModalFormContentH,
                vertical: AppSizeMarginPadding.paddingModalFormContentV,
              ),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(AppSizeMarginPadding.cardRadiusDefault),
                  bottomLeft: Radius.circular(AppSizeMarginPadding.cardRadiusDefault),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildModalHeader(),
                  widget.child,
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  /// Método para criar o Header do modal
  /// contendo o titulo e o botão de fechar
  ///
  Widget _buildModalHeader() {
    return Row(
      children: [
        Text(widget.title, style: AppTitleModalFormatStyle.style()),
        const Spacer(),
        IconButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          icon: const Icon(Icons.close),
        ),
      ],
    );
  }

  /// Método para criar o container que
  /// ocupará toda a tela, dando o efeito de modal
  ///
  Widget _buildModalBackground() {
    return GestureDetector(
      onTap: () {
        Navigator.of(context).pop();
      },
      child: Container(
        width: MediaQuery.sizeOf(context).width * .30,
        color: AppColors.transparent,
      ),
    );
  }
}
