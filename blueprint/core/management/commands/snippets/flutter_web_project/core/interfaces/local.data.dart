import 'package:either_dart/either.dart';

/// Interface para camada de persistência de dados locais
///
/// Essa interface define os métodos que devem ser implementados
/// pelas classes que fazem a persistência de dados locais.
///
/// Os métodos são genéricos e podem retornar diferentes tipos de dados.
///
/// Os métodos retornam um objeto Either, onde o primeiro valor é uma
/// exceção (Exception) e o segundo valor é o resultado da operação.
///
abstract class LocalDataInterface {
  /// Método para verificar se a base de dados foi
  /// inicializada
  ///
  /// Return:
  ///   Either<Exception, bool> - Retorna true se a base de dados foi inicializada
  ///
  Future<Either<Exception, bool>> isInitialized();

  /// Método para buscar todos dados locais
  ///
  /// Return:
  ///   Either<Exception, List<T>> - Retorna o resultado da operação
  ///
  Future<Either<Exception, List<T>>> fetch<T>();

  /// Método para buscar um item no banco de dados local
  ///
  /// Params:
  ///  [id] - int - ID do item a ser buscado
  ///
  /// Return:
  ///  Either<Exception, T> - Retorna o resultado da operação
  ///
  Future<Either<Exception, T>> get<T>({required int id});

  /// Método para inserir um item no banco de dados local
  ///
  /// Params:
  /// [data] - T - Dados a serem inseridos
  ///
  /// Return:
  /// Either<Exception, T> - Retorna o resultado da operação
  ///
  Future<Either<Exception, bool>> insert<T>(T data);

  /// Método para atualizar um item no banco de dados local
  ///
  /// Params:
  /// [data] - T - Dados a serem atualizados
  ///
  /// Return:
  /// Either<Exception, T> - Retorna o resultado da operação
  ///
  Future<Either<Exception, T>> update<T>(T data);

  /// Método para deletar um item no banco de dados local
  ///
  /// Params:
  /// [id] - int - ID do item a ser deletado
  ///
  /// Return:
  /// Either<Exception, bool> - Retorna o resultado da operação
  ///
  Future<Either<Exception, bool>> delete({required int id});

  /// Método para deletar todos os itens no banco de dados local
  ///
  /// Return:
  /// Either<Exception, bool> - Retorna o resultado da operação
  ///
  Future<Either<Exception, bool>> deleteAll();
}
