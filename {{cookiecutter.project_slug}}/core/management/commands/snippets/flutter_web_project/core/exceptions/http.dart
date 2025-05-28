/// Enum com os exceptions possíveis para o HttpInterface
///
library;

enum HttpException {
  /// Erro de timeout
  timeout,

  /// Erro de conexão
  connection,

  /// Erro de resposta inválida
  invalidResponse,

  /// Erro de URL inválida
  invalidUrl,

  /// Erro de servidor
  serverError,

  /// Erro desconhecido
  unknown,
}
