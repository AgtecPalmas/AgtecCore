import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';

const defaultBackgroundColor = AppColors.buttonSolidGreenBackground;
const defaultForegroundColor = AppColors.buttonSolidGreenText;
const defaultOutlineBackgroundColor = AppColors.transparent;
const defaultOutlineForegroundColor = AppColors.buttonOutlinedGreenText;
const defaultOutlineBorderColor = AppColors.buttonOutlinedGreenBackground;

class AppButtonPrimaryStyle {
  static ButtonStyle style() {
    return ElevatedButton.styleFrom(
      backgroundColor: defaultBackgroundColor,
      foregroundColor: defaultForegroundColor,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(
          AppSizeMarginPadding.buttonDefaultRadius,
        ),
      ),
      padding: const EdgeInsets.symmetric(
        vertical: AppSizeMarginPadding.paddingButtonDefaultV,
        horizontal: AppSizeMarginPadding.paddingButtonDefaultH,
      ),
      minimumSize: const Size(
        AppSizeMarginPadding.buttonW,
        AppSizeMarginPadding.buttonH,
      ),
    );
  }
}

class AppButtonOutlinedStyle {
  static ButtonStyle style() {
    return OutlinedButton.styleFrom(
      side: const BorderSide(color: defaultOutlineBorderColor),
      backgroundColor: AppColors.transparent,
      foregroundColor: defaultOutlineForegroundColor,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(
          AppSizeMarginPadding.buttonDefaultRadius,
        ),
      ),
      padding: const EdgeInsets.symmetric(
        vertical: AppSizeMarginPadding.paddingButtonDefaultV,
        horizontal: AppSizeMarginPadding.paddingButtonDefaultH,
      ),
      minimumSize: const Size(
        AppSizeMarginPadding.buttonW,
        AppSizeMarginPadding.buttonH,
      ),
    );
  }
}

class AppButtonTextStyle {}
