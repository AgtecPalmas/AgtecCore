import 'package:either_dart/either.dart';

/// Interface para a camada de HTTP
/// Essa interface define os métodos que devem ser implementados
/// pelas classes que fazem requisições HTTP.
///
/// Os métodos são genéricos e podem retornar diferentes tipos de dados.
///
/// Os métodos retornam um objeto Either, onde o primeiro valor é uma
/// exceção (Exception) e o segundo valor é o resultado da requisição.
///
abstract class HttpInterface {
  /// Método responsável por fazer a requisição GET
  /// retornando todos os registros, paginados conforme
  /// definição do backend.
  ///
  /// Params:
  ///   [uri] - String? - URI da requisição
  ///   [returnResult] - bool - Se true, retorna o resultado da requisição
  ///
  /// Return:
  ///  [Either<Exception, List<T>>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, List<T>>> fetch<T>({
    returnResult = false,
  });

  /// Método responsável por fazer a requisição GET
  /// retornando todos os registros, paginados conforme
  /// definição do backend.
  ///
  /// Params:
  ///  [uri] - String? - URI da requisição
  ///  [returnResult] - bool - Se true, retorna o resultado da requisição
  ///
  /// Return:
  ///  [Either<Exception, List<T>>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, List<T>>> getMore<T>({
    required String uri,
    returnResult = false,
  });

  /// Método responsável por fazer a requisição GET
  /// retornando um único registro.
  ///
  /// Params:
  ///  [id] - String - ID do recurso a ser recuperado
  ///
  /// Return:
  ///  [Either<Exception, T>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, T>> detail<T>({
    required String id,
  });

  /// Método responsável por fazer a requisição POST
  /// enviando dados para o backend.
  ///
  /// Params:
  ///  [data] - dynamic - Dados a serem enviados na requisição
  ///  [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  ///  [Either<Exception, T>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, T>> post<T>({
    required dynamic data,
    bool multipart = false,
  });

  /// Método responsável por fazer a requisição PUT
  /// enviando dados para o backend.
  ///
  /// Params:
  ///  [data] - dynamic - Dados a serem enviados na requisição
  ///  [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  ///  [Either<Exception, T>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, T>> put<T>({
    required dynamic data,
    bool multipart = false,
  });

  /// Método responsável por fazer a requisição PATCH
  /// enviando dados para o backend.
  ///
  /// Params:
  ///  [data] - dynamic - Dados a serem enviados na requisição
  ///  [multipart] - bool - Se true, o conteúdo será enviado como multipart/form-data
  ///
  /// Return:
  ///  [Either<Exception, T>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, T>> patch<T>({
    required dynamic data,
    bool multipart = false,
  });

  /// Método responsável por fazer a requisição DELETE
  /// removendo um registro do backend.
  ///
  /// Params:
  ///  [id] - String - ID do recurso a ser removido
  ///
  /// Return:
  ///  [Either<Exception, bool>] - Retorna o resultado da requisição
  ///
  Future<Either<Exception, bool>> delete({required String id});
}
