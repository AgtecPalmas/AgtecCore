/// [Arquivo gerado automatimante pelo NuvolsCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração do pacote Dio, e que não deve ser alterado
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///
library;
import 'dart:async';

import 'package:dio/dio.dart';
import 'package:either_dart/either.dart';
import '/core/app.config.dart';
import '/core/app.logger.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

class AppDio {
  late Dio _dio;
  String _url = '';

  AppDio(
    String url, {
    String? authenticationToken,
    String? errorMessage,
    String? token,
    String contentType = 'application/json; charset=utf-8',
    bool unAuthenticated = false,
  }) {
    _url = url;

    final BaseOptions options = BaseOptions(
      baseUrl: url,
      connectTimeout: const Duration(seconds: 60),
      receiveTimeout: const Duration(seconds: 60),
    );
    if (unAuthenticated == false) {
      if (token != null) {
        options.headers = {'Authorization': 'Bearer $token'};
      } else if (authenticationToken != null) {
        options.headers = {'Authorization': 'Token $authenticationToken'};
      } else {
        options.headers = {'Authorization': Config.drfToken};
      }
    }
    _dio = Dio(options)
      ..interceptors.add(
        PrettyDioLogger(requestBody: true, requestHeader: true),
      );

    // if (releaseVersion == false) {
    //   _dio.interceptors.add(RefreshTokenInterceptor(customDio: this, dio: _dio));
    // }
  }

  /// [_clearErrorMessageString]
  /// Método que limpar a string de erro retornada pelo Backend
  ///
  /// Returns:
  ///   [error] - String - String de erro retornada pelo Backend
  ///
  String clearErrorMessage(String? errorMessage) {
    try {
      if (errorMessage == null) return '';
      errorMessage = errorMessage.replaceAll('{', '').replaceAll('}', '');
      final errorMessageSplit = errorMessage.split('[').last.replaceAll(']', '');
      return errorMessageSplit;
    } catch (e) {
      return '';
    }
  }

  /// Método responsável por fazer a requisição GET
  ///
  /// Params:
  ///   [uri] - String? - URI da requisição
  ///   [returnResult] - bool - Se true, retorna o resultado da requisição
  /// Return:
  ///   Either<Exception, dynamic> - Retorna o resultado da requisição
  ///

  Future<Either<Exception, dynamic>> get({String? uri, returnResult = false}) async {
    try {
      NuvolsCoreLogger().info('#dio_custom URl: $_url');
      NuvolsCoreLogger().info('#dio_custom Dio Headers: ${_dio.options.headers}');
      final Response response = await _dio.get(uri ?? _url);
      if (response.statusCode == 200) {
        NuvolsCoreLogger().info('#dio_custom Retorno do método getHTTP');
        NuvolsCoreLogger().verbose(response);
        if (returnResult) return response.data['results'];
        return Right(response.data);
      }
      return Left(Exception('Erro ao retornar os dados, statusCode: ${response.statusCode}'));
    } on DioException catch (error) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método getHTTP: ${error.message}', error);
      return Left(Exception(error));
    } catch (errorGeneral) {
      return Left(Exception(errorGeneral));
    }
  }

  /// Método responsável por fazer a requisição POST
  ///
  /// Params:
  ///   [uri] - String? - URI da requisição
  ///   [data] - dynamic - Dados a serem enviados na requisição
  ///   [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  ///  Either<Exception, dynamic> - Retorna o resultado da requisição
  ///
  Future<Either<Exception, dynamic>> post({
    String? uri,
    required dynamic data,
    bool multipart = false,
  }) async {
    try {
      if (multipart == true) {
        _dio.options.headers['Content-Type'] = 'multipart/form-data';
      }
      final Response response = await _dio.post(uri ?? _url, data: data);
      if (response.statusCode == 201 || response.statusCode == 200) {
        NuvolsCoreLogger().info('#dio_custom Retorno do método post');
        NuvolsCoreLogger().verbose(response);
        return Right(response.data);
      }
      return Left(Exception('Erro ao retornar os dados, statusCode: ${response.statusCode}'));
    } on DioException catch (error) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método post: ${error.message}', error);
      return Left(Exception(error));
    } catch (errorGeneral) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método post: $errorGeneral', errorGeneral);
      return Left(Exception(errorGeneral));
    }
  }

  /// Método responsável por fazer a requisição PUT
  ///
  /// Params:
  ///   [uri] - String? - URI da requisição
  ///   [data] - dynamic - Dados a serem enviados na requisição
  ///   [id] - String - ID do recurso a ser atualizado
  ///   [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  /// Either<Exception, dynamic> - Retorna o resultado da requisição
  ///
  Future<Either<Exception, dynamic>> put({
    String? uri,
    required dynamic data,
    required String id,
    bool multipart = false,
  }) async {
    try {
      if (multipart == true) {
        _dio.options.headers['Content-Type'] = 'multipart/form-data';
      }
      final Response response = await _dio.put(uri ?? _url, data: data);
      if (response.statusCode == 201 || response.statusCode == 200) {
        NuvolsCoreLogger().info('#dio_custom Retorno do método put');
        NuvolsCoreLogger().verbose(response);
        return Right(response.data);
      }
      return Left(Exception('Erro ao retornar os dados, statusCode: ${response.statusCode}'));
    } on DioException catch (error) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método put: ${error.message}', error);
      return Left(Exception(error));
    } catch (errorGeneral) {
      return Left(Exception(errorGeneral));
    }
  }

  /// Método responsável por fazer a requisição PATCH
  ///
  /// Params:
  ///  [uri] - String? - URI da requisição
  ///  [data] - dynamic - Dados a serem enviados na requisição
  ///  [id] - String - ID do recurso a ser atualizado
  ///  [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  ///  Either<Exception, dynamic> - Retorna o resultado da requisição
  ///
  Future<Either<Exception, dynamic>> patch({
    String? uri,
    required dynamic data,
    required String id,
    bool multipart = false,
  }) async {
    try {
      if (multipart == true) {
        _dio.options.headers['Content-Type'] = 'multipart/form-data';
      }
      final Response response = await _dio.patch(uri ?? _url, data: data);
      if (response.statusCode == 201 || response.statusCode == 200) {
        NuvolsCoreLogger().info('#dio_custom Retorno do método patchHTTP');
        NuvolsCoreLogger().verbose(response);
        return Right(response.data);
      }
      return Left(Exception('Erro ao retornar os dados, statusCode: ${response.statusCode}'));
    } on DioException catch (error) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método patchHTTP: ${error.message}', error);
      return Left(Exception(error));
    } catch (errorGeneral) {
      return Left(Exception(errorGeneral));
    }
  }

  /// Método responsável por fazer a requisição DELETE
  ///
  /// Params:
  ///   [uri] - String? - URI da requisição
  ///   [id] - String - ID do recurso a ser excluído
  ///
  /// Return:
  ///  Either<Exception, dynamic> - Retorna o resultado da requisição
  ///
  Future<Either<Exception, dynamic>> delete({String? uri, required String id}) async {
    try {
      final Response response = await _dio.delete(uri ?? _url);
      if (response.statusCode == 200 || response.statusCode == 204) {
        NuvolsCoreLogger().info('#dio_custom Retorno do método deleteHTTP');
        NuvolsCoreLogger().verbose(response);
        return Right(response.data);
      }
      return Left(Exception('Erro ao retornar os dados, statusCode: ${response.statusCode}'));
    } on DioException catch (error) {
      NuvolsCoreLogger().erro('#dio_custom Erro no método deleteHTTP: ${error.message}', error);
      return Left(Exception(error));
    } catch (errorGeneral) {
      return Left(Exception(errorGeneral));
    }
  }
}
