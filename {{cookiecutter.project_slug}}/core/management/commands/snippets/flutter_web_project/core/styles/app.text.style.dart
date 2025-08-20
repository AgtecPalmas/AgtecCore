import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.fonts.dart';

/// Estilo de texto para o título do menu
class AppTitleMenuStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textMenuTitle,
      fontSize: AppFont.appNameSize,
      fontWeight: FontWeight.w800,
      fontFamily: 'Inter',
      fontStyle: FontStyle.normal,
    );
  }
}

class AppMenuItemStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textMenuLabelItem,
      fontSize: AppFont.menuItemSize,
      fontWeight: FontWeight.w700,
      fontFamily: 'Inter',
    );
  }

  static TextStyle styleSelected() {
    return const TextStyle(
      color: AppColors.menuItemActivatedText,
      fontSize: AppFont.menuItemSize,
      fontWeight: FontWeight.w700,
      fontFamily: 'Inter',
    );
  }
}

class AppTextStyle {}

/// Estilo de texto para os títulos das
/// páginas
class AppTextTitlePageStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textTitlePage,
      fontSize: AppFont.appNameSize,
      fontWeight: FontWeight.w800,
      fontFamily: 'Inter',
    );
  }
}

/// Estilo de texto para os
/// títulos dos cards
class AppTitleCardStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textTitleCard,
      fontSize: AppFont.titleCardSize,
      fontWeight: FontWeight.w600,
      fontFamily: 'Inter',
    );
  }
}

class AppTableHeaderStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textTableHeader,
      fontSize: AppFont.tableHeaderSize,
      fontWeight: FontWeight.w500,
      fontFamily: 'Inter',
    );
  }
}

class AppTableItemStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textTableItemEnable,
      fontSize: AppFont.titleCardSize,
      fontWeight: FontWeight.w400,
      fontFamily: 'Inter',
    );
  }
  static TextStyle disabled() {
    return const TextStyle(
      color: AppColors.textTableItemDisable,
      fontSize: AppFont.titleCardSize,
      fontWeight: FontWeight.w400,
      fontFamily: 'Inter',
    );
  }
}

// UsernameStyle
class AppUserNameStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.userName,
      fontSize: AppFont.userNameSize,
      fontWeight: FontWeight.w800,
      fontFamily: 'Inter',
    );
  }
}

// UsernameStyle
class AppTitleModalFormatStyle {
  static TextStyle style() {
    return const TextStyle(
      color: AppColors.textTitleModalForm,
      fontSize: AppFont.modalFormTitleSize,
      fontWeight: FontWeight.w800,
      fontFamily: 'Inter',
    );
  }
}
