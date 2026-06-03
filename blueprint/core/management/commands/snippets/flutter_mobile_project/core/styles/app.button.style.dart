import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';

const defaultBackgroundColor = AppColors.listViewPageBottomSheetPrimaryButtonBackground;
const defaultForegroundColor = AppColors.listViewPageBottomSheetBackground;
const defaultOutlineBackgroundColor = AppColors.transparent;
const defaultOutlineForegroundColor = AppColors.listViewPageBottomSheetChildrensForeground;
const defaultOutlineBorderColor = AppColors.listViewPageBottomSheetChildrensForeground;

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
      backgroundColor: defaultOutlineBackgroundColor,
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

class AppCancelButtonBottomSheetOutlinedStyle {
  static ButtonStyle style() {
    return OutlinedButton.styleFrom(
      side: const BorderSide(color: AppColors.listViewPageBottomSheetSecondaryButtonBackground),
      backgroundColor: AppColors.listViewPageBottomSheetSecondaryButtonBackground,
      foregroundColor: AppColors.listViewPageBottomSheetSecondaryButtonForeground,
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

