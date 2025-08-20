import 'package:flutter/material.dart';

import '../../constants/app.colors.dart';
import '../../constants/app.sizes.dart';

class AppCardStyle {
  static BorderSide style() {
    return const BorderSide(
      color: AppColors.cardBorder,
      width: AppSizeMarginPadding.borderCardW,
    );
  }
}
