///
/// [Arquivo gerado automaticamente pelo AgtecCore ]
///

/// [Descrição]
/// Arquivo responsável por definir as rotas do projeto.
/// que será utilizado para navegar entre as telas do app.
/// as rotas de cada app serão apensadas neste arquivo.
///


///
/// [Arquivo travado]
///
/// Para evitar que o arquivo seja reescrito acidentalmente, 
/// o mesmo encontra-se "travado", para destravar remova o # da linha abaixo.
/// 
/// #FileLocked
///

import 'package:go_router/go_router.dart';

import '../apps/dashboard/pages/dashboard.dart';
import '../apps/settings/pages/settings.dart';

$ImportRouters$

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
      path: '/settings',
      name: 'configuracao',
      builder: (context, state) {
        return const SettingsPage(title: 'Configurações');
      },
    ),
    // Incorporando as rotas de cada app
    $AppsRouters$
  ],
);
