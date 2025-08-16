///
/// [Arquivo gerado automatimante pelo AgtecCore ]
///

/// 
/// [Travado por default]
/// Por ser um arquivo de configuração, para evitar que o mesmo seja sobrescrito
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///

///
///  [Exemplo de uso]
///    AppLogger().info("Apenas uma informação teste");
///    AppLogger().erro("Erro", "", StackTrace.current);
///    AppLogger.debug("Debug", "", StackTrace.current);
///    AppLogger.warning("Warning", "", StackTrace.current);
///    AppLogger.crash("Crash", "", StackTrace.current);
///    AppLogger().verbose({"chave": "valor"});
///

import 'package:flutter/foundation.dart';
import 'package:logger/logger.dart';

/// Classe com métodos abstratos para gerar logs costomizados
///
/// [Exemplo de uso]
/// ```
/// AppLogger().info("Apenas uma informação teste");
/// ```
/// ```
/// AppLogger().erro("Erro", "", StackTrace);
/// ```
/// ```
/// AppLogger.debug("Debug", "", StackTrace.current);
/// ```
/// ```
/// AppLogger.warning("Warning", "", StackTrace.current);
/// ```
/// ```
/// AppLogger.crash("Crash", "", StackTrace);
/// ```
/// ```
/// AppLogger().verbose({"chave": "valor"});
/// ```
class AppLogger {
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
