///
/// Guarda para controlar as rotas que necessitam de autenticação
///
library;

import 'package:go_router/go_router.dart';
import '/core/guards/route_guard.dart';

class AuthGuard implements RouteGuard {
  AuthGuard({this.invert = false});

  final bool invert;

  @override
  String? call(GoRouterState state) {
    // TODO Implementar lógica para verificar se o usuário está logado.

    // final AuthRepository authRepository = getIt();
    // if (authRepository.authTokens == null && !invert) {
    //   return '/sign-in?redirectTo=${state.matchedLocation}';
    // } else if (authRepository.authTokens != null && invert) {
    //   return '/stores';
    // }

    return null;
  }
}
