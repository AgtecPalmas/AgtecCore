/// Enum com os exceptions possíveis para o AuthInterface
///


enum AuthException {
  /// Erro de autenticação
  authentication,

  /// Erro de autorização
  authorization,

  /// Erro de token expirado
  tokenExpired,

  /// Erro de token inválido
  invalidToken,

  /// Usuario não encontrado
  userNotFound,

  /// Email não encontrado
  emailNotFound,

  /// Erro desconhecido
  unknown,
}
