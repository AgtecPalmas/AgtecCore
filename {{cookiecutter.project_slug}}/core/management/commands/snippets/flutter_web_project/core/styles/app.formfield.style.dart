import 'package:flutter/material.dart';
import '/constants/app.sizes.dart';

import '../../constants/app.colors.dart';

class AppInputTextFormFieldStyle {
  static InputDecoration style({
    String hintText = '',
    bool hiddenCounter = false,
  }) {
    return InputDecoration(
      hintText: hintText,
      counter: hiddenCounter ? const Offstage() : null,
      floatingLabelBehavior: FloatingLabelBehavior.never,
      contentPadding: const EdgeInsets.only(
        left: AppSizeMarginPadding.paddingInputTextFormFieldHintL,
        top: AppSizeMarginPadding.paddingInputTextFormFieldHintT,
        bottom: AppSizeMarginPadding.paddingInputTextFormFieldHintB,
      ),
      hintStyle: const TextStyle(
        color: AppColors.textFormFieldHint,
        fontSize: 14,
        fontStyle: FontStyle.normal,
        fontWeight: FontWeight.w400,
      ),
      errorStyle: const TextStyle(
        fontSize: 12,
        color: AppColors.errorDefaultRed,
        fontWeight: FontWeight.w400,
      ),
      isDense: true,
      errorBorder: InputBorder.none,
      border: InputBorder.none,
      focusedErrorBorder: InputBorder.none,
    );
  }
}
