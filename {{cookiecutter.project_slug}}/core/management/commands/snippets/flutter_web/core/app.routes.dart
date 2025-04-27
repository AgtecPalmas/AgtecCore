import 'package:go_router/go_router.dart';

import '../apps/auth/pages/sigin.dart';
import '../apps/products/pages/products.dart';
import '../apps/settings/pages/settings.dart';

///
/// Arquivo para controlar as rotas principais do app
/// as rotas internas das app serão injetadas
/// aqui teremos apenas as rotas principais
///  dashboard
///  login
///  logout
///  settings
///
///

final appRouter = GoRouter(
  initialLocation: '/dashboard',
  debugLogDiagnostics: true,
  redirectLimit: 10,
  routes: <RouteBase>[
    GoRoute(
      path: '/dashboard',
      name: 'dashboard',
      builder: (context, state) {
        return const DashboardPage(title: 'Titulo');
      },
    ),
    GoRoute(
      path: '/products',
      name: 'products',
      builder: (context, state) {
        return const ProductPage(title: 'Produtos');
      },
    ),
    GoRoute(
      path: '/settings',
      name: 'configuracao',
      builder: (context, state) {
        return const SettingsPage(title: 'Configurações');
      },
    ),
  ],
);
