///
/// [Arquivo gerado automatimante pelo AgtecCore ]
///
/// [Travado por default]
///
/// Por ser um mixin de padronização das mensagens, e que não deve ser alterado
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///

import 'package:flutter/material.dart';
import 'package:top_snackbar_flutter/custom_snack_bar.dart';
import 'package:top_snackbar_flutter/top_snack_bar.dart';
import '../constants/app.colors.dart';

///
/// Mixin para facilitar a exibição de mensagens na tela.
/// Para utilizar o mixin, basta adicionar o código [with Messages]
/// na classe que deseja utilizar o mixin, Lembrando que a
/// classe deve extender de [StatefulWidget].e o comando
/// deve ser adicionado na class State<T> da classe
/// Ex:. [class _SplashScreenPageState extends State<SplashScreenPage> with Messages {]
///
mixin MessagesMixin<T extends StatefulWidget> on State<T> {
  void showError(String message) {
    showTopSnackBar(
      Overlay.of(context),
      CustomSnackBar.error(message: message),
    );
  }

  void showInfo(String message) {
    showTopSnackBar(
      Overlay.of(context),
      CustomSnackBar.info(message: message),
    );
  }

  void showSuccess(String message) {
    showTopSnackBar(
      Overlay.of(context),
      CustomSnackBar.success(message: message),
    );
  }

  void showWarning(String message) {
    showTopSnackBar(
      Overlay.of(context),
      CustomSnackBar.info(
        message: message,
        backgroundColor: AppColors.warningBackgroundSnackBarMessage,
        icon: const Icon(
          Icons.warning,
          color: AppColors.warningIconColorSnackBarMessage,
          size: 120,
        ),
      ),
    );
  }
}
