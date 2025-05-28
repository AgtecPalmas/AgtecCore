import 'package:go_router/go_router.dart';

/// Interface responsável por definir as guardas
/// para as rotas
///
///

abstract interface class RouteGuard {
  /// Método responsável por verificar se a rota pode ser acessada
  ///
  /// Retorna um booleano indicando se a rota pode ser acessada ou não

  String? call(GoRouterState state);

  static String? apply(GoRouterState state, List<RouteGuard> guards) {
    for (final guard in guards) {
      final redirect = guard(state);
      if (redirect != null) {
        return redirect;
      }
    }
    return null;
  }
}
