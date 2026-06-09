///
/// [Arquivo gerado automatimante pelo AgtecCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração do pacote Dio, e que não deve ser alterado
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///

import 'package:dio/dio.dart';

import '../../app.config.dart';

final class HeaderTokenInterceptor extends Interceptor {
  @override
  Future<void> onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    const String accessToken = ''; // await AuthData().getJWTToken();
    if (accessToken.isNotEmpty) {
      options.headers.addAll({'Authorization': 'Bearer $accessToken'});
    } else {
      options.headers.addAll({'Authorization': Config.drfToken});
    }
    options.connectTimeout = const Duration(seconds: 20);
    options.receiveTimeout = const Duration(seconds: 20);
    return super.onRequest(options, handler);
  }
}
