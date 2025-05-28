import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

class AppModal extends StatefulWidget {
  const AppModal({super.key, required this.child, required this.title});

  final Widget child;
  final String title;

  @override
  State<AppModal> createState() => _AppModalState();
}

class _AppModalState extends State<AppModal> {
  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.modalFormBackground,
      child: GestureDetector(
        onTap: () {
          Navigator.of(context).pop();
        },
        child: Container(
          width: double.infinity,
          height: double.infinity,
          margin: const EdgeInsets.symmetric(
            vertical: AppSizeMarginPadding.marginModalFormBottom,
          ),
          padding: const EdgeInsets.all(0),
          color: AppColors.transparent,
          child: Center(
            child: LayoutBuilder(
              builder: (BuildContext contextLB, BoxConstraints constraints) {
                return Container(
                  constraints: BoxConstraints(
                    maxHeight: MediaQuery.sizeOf(context).height * .50,
                    minHeight: MediaQuery.sizeOf(context).height * .45,
                    maxWidth: MediaQuery.sizeOf(context).width * .70,
                    minWidth: MediaQuery.sizeOf(context).width * .30,
                  ),
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSizeMarginPadding.paddingModalFormContentH,
                    vertical: AppSizeMarginPadding.paddingModalFormContentV,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.cardBackground,
                    borderRadius: BorderRadius.circular(
                      AppSizeMarginPadding.cardRadiusDefault,
                    ),
                    border: Border.all(
                      color: AppColors.cardBorder,
                      width: 1,
                    ),
                  ),
                  child: Column(
                    children: [
                      _buildModalHeader(),
                      const SizedBox(height: 16),
                      widget.child,
                    ],
                  ),
                );
              },
            ),
          ),
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
}
