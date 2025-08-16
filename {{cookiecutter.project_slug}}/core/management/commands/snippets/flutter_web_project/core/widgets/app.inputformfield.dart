import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.fonts.dart';
import '/constants/app.sizes.dart';

class AppWidgetContainerInputFormField extends StatelessWidget {
  // Classe para retornar o componente InputFormField com os padrões do
  // design system da Agtec
  final String labelText;
  final TextFormField textFormField;

  const AppWidgetContainerInputFormField({
    super.key,
    required this.labelText,
    required this.textFormField,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.textFormFieldContainerParentBackground,
        borderRadius: BorderRadius.circular(AppSizeMarginPadding.textInputRadius),
        border: Border.all(
          color: AppColors.textFormFieldBorder,
          width: AppSizeMarginPadding.inputTextFormFieldBorderSize,
        ),
      ),
      margin: const EdgeInsets.only(
        top: AppSizeMarginPadding.marginContainerParentInputTextFormFieldT,
        right: AppSizeMarginPadding.marginContainerParentInputTextFormFieldR,
        bottom: AppSizeMarginPadding.marginContainerParentInputTextFormFieldB,
      ),
      padding: const EdgeInsets.only(
        left: AppSizeMarginPadding.paddingInputTextFormFieldL,
        top: AppSizeMarginPadding.paddingInputTextFormFieldT,
        bottom: AppSizeMarginPadding.paddingInputTextFormFieldB,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            labelText,
            style: const TextStyle(
              color: AppColors.textFormFieldLabel,
              fontSize: AppFont.inputTextLabelSize,
            ),
          ),
          const SizedBox(
            height: AppSizeMarginPadding.inputTextFormFieldLabelToContentHintSpaceV,
          ),
          textFormField,
        ],
      ),
    );
  }
}
