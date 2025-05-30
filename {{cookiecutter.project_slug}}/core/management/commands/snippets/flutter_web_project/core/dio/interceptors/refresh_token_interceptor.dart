///
/// [Arquivo gerado automatimante pelo NuvolsCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração do pacote Dio, e que não deve ser alterado
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///


import 'package:dio/dio.dart';
import '/core/app.config.dart';
import '/core/app.logger.dart';

/// Interceptor específico para gerenciamento do
/// fluxo de atualização do RefreshToken
final class RefreshTokenInterceptor extends Interceptor {
  final String _refreshTokenPath = '${Config.uri}api/token/refresh/';

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    // Verificando o tipo do erro baseado no status code do response
    try {
      final errorResponse = err.response;
      final requestPath = err.requestOptions.path;

      if (errorResponse != null) {
        final statusCode = errorResponse.statusCode;
        // Verificando se o statusCode é 403 ou 401
        if (statusCode == 403 || statusCode == 401) {
          // Verificando se o path do endPoint é o de refreshToken
          if (requestPath != _refreshTokenPath) {
            // await _refreshToken(err);
            // Chamando o método para realizar a retentativa da consulta
            // await _retryRequest(err);
          } else {
            AppLogger().debug('Ocorreu o erro: $err | StackTrace: ${StackTrace.current}');
            throw err;
          }
        } else {
          // Erro não é 403 nem 401
          AppLogger().debug('Ocorreu o erro: $err | StackTrace: ${StackTrace.current}');
          // Passando o erro para cima, quem chamou a requisição
          throw err;
        }
      }
    } on DioException catch (err, stackTrace) {
      AppLogger().erro('Ocorreu o erro: $err ao atualizar o RefreshToken | StackTrace: $stackTrace', err);
      // Passando o erro para cima, quem chamou a requisição
      handler.next(err);
    } catch (error, stackTrace) {
      AppLogger().erro('Ocorreu o erro: $err | StackTrace: $stackTrace', error);
      // Passando o erro para cima, quem chamou a requisição
      handler.next(err);
    }
  }
}
