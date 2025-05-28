import 'package:get_it/get_it.dart';
import '../apps/auth/models/auth.dart';
import '../core/app.config.dart';
import '../core/dio/app_dio.dart';

///
/// Arquivo para gerenciar as injeções de dependência do projeto
/// utilzando o GetIt
///

final getIt = GetIt.I;

/// Método para registrar as dependências
///
void configureDependencies() {
  // Aqui você pode registrar suas dependências
  // Exemplo:
  // getIT.registerLazySingleton<SomeService>(() => SomeServiceImpl());

  /// Adicionando o CustomDio
  getIt.registerSingleton<AppDio>(AppDio(Config.fastAPIURI));

  /// Adicionando o AuthModel
  getIt.registerSingleton<AuthModel>(AuthModel());
}
