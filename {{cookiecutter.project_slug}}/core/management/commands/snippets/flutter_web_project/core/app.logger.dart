/// [Arquivo gerado automatimante pelo NuvolsCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração, para evitar que o mesmo seja sobrescrito
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///
// ignore_for_file: public_member_api_docs, sort_constructors_first
/// Classe para centralizar as mensagens de logg do desenvolvimento
/// Utilizo o pacote logger na versão logger: ^1.1.0 para controlar o
/// visual dos logs
/// Url Pacote: https://pub.dev/packages/logger/example
/// [Exemplo de uso]
///    NuvolsCoreLogger().info("Apenas uma informação teste");
///    NuvolsCoreLogger().erro("Erro", "", StackTrace.current);
///    NuvolsCoreLogger.debug("Debug", "", StackTrace.current);
///    NuvolsCoreLogger.warning("Warning", "", StackTrace.current);
///    NuvolsCoreLogger.crash("Crash", "", StackTrace.current);
///    NuvolsCoreLogger().verbose({"chave": "valor"});
///
library;
import 'package:flutter/foundation.dart';
import 'package:logger/logger.dart';

/// Classe com métodos abstratos para gerar logs costomizados
///
/// [Exemplo de uso]
/// ```
/// NuvolsCoreLogger().info("Apenas uma informação teste");
/// ```
/// ```
/// NuvolsCoreLogger().erro("Erro", "", StackTrace);
/// ```
/// ```
/// NuvolsCoreLogger.debug("Debug", "", StackTrace.current);
/// ```
/// ```
/// NuvolsCoreLogger.warning("Warning", "", StackTrace.current);
/// ```
/// ```
/// NuvolsCoreLogger.crash("Crash", "", StackTrace);
/// ```
/// ```
/// NuvolsCoreLogger().verbose({"chave": "valor"});
/// ```
class NuvolsCoreLogger {
  final Logger _logger = Logger();

  void erro(dynamic message, dynamic error, [StackTrace? stackTrace]) {
    if (kDebugMode) _logger.e(message, error: error, stackTrace: StackTrace.current);
  }

  void info(dynamic message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) _logger.i(message, error: error, stackTrace: stackTrace);
  }

  void debug(dynamic message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) _logger.d(message, error: error, stackTrace: stackTrace);
  }

  void warning(dynamic message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) _logger.w(message, error: error, stackTrace: stackTrace);
  }

  void crash(dynamic message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) _logger.i(message, error: error, stackTrace: stackTrace);
  }

  void verbose(dynamic message) {
    if (kDebugMode) _logger.i(message);
  }

  void homolog(dynamic message) {
    _logger.i(message);
  }
}
