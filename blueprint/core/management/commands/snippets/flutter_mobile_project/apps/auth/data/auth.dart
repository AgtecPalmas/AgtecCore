import 'package:either_dart/either.dart';
import '/apps/auth/models/auth.dart';
import '/core/app.logger.dart';
import '/core/interfaces/local.data.dart';

/// Classe para controlar o DB local que utiliza o pacote SembastWeb
/// dados sensíveis não devem ser armazenados no DB local
///
///

class AuthData implements LocalDataInterface {
  AuthModel authModel = AuthModel.empty();

  @override
  Future<Either<Exception, bool>> isInitialized() async {
    try {
      // Implementado a lógica para verificar se o banco de dados foi inicializado

      return const Right(true);
    } catch (error, stackTrace) {
      AppLogger().erro('Error initializing database', error, stackTrace);
      return Left(Exception('Error initializing database'));
    }
  }

  /// Método para atualizar um item no banco de dados local
  ///
  /// Params:
  ///  [data] - AuthModel - Dados a serem atualizados
  ///
  /// Return:
  ///   Either<Exception, AuthModel> - Retorna o resultado da operação
  /// 
  @override
  Future<Either<Exception, AuthModel>> update<AuthModel>(AuthModel data) async {
    try {
      // Implementado a lógica para atualizar o banco de dados local
      return Right(data);
    } catch (error, stackTrace) {
      AppLogger().erro('Error updating database', error, stackTrace);
      return Left(Exception('Error updating database'));
    }
  }

  /// Método para deletar um item no banco de dados local
  ///
  /// Params:
  ///  [id] - int - ID do item a ser deletado
  ///
  /// Return:
  ///  Either<Exception, bool> - Retorna o resultado da operação
  ///
  @override
  Future<Either<Exception, bool>> delete({required int id}) async {
    try {
      // Implementado a lógica para deletar o item do banco de dados local
      return const Right(true);
    } catch (error, stackTrace) {
      AppLogger().erro('Error deleting item from database', error, stackTrace);
      return Left(Exception('Error deleting item from database'));
    }
  }

  /// Método para deletar todos os itens AuthModel no banco de dados local
  ///
  /// Return:
  ///  Either<Exception, bool> - Retorna o resultado da operação
  ///
  @override
  Future<Either<Exception, bool>> deleteAll() async {
    try {
      return const Right(true);
    } catch (error, stackTrace) {
      AppLogger().erro('Error deleting all items from database', error, stackTrace);
      return Left(Exception('Error deleting all items from database'));
    }
  }

  /// Método para buscar todos os AuthModels dados locais
  ///
  /// Return:
  ///  Either<Exception, List<AuthModel>> - Retorna o resultado da operação
  ///
  @override
  Future<Either<Exception, List<AuthModel>>> fetch<AuthModel>() async {
    try {
      List<AuthModel> authModels = [];
      // Implementado a lógica para buscar todos os dados do banco de dados local
      return Right(authModels);
    } catch (error, stackTrace) {
      AppLogger().erro('Error fetching data from database', error, stackTrace);
      return Left(Exception('Error fetching data from database'));
    }
  }

  /// Método para buscar um item no banco de dados local
  ///
  /// Params:
  ///  [id] - int - ID do item a ser buscado
  ///
  /// Return:
  ///  Either<Exception, AuthModel> - Retorna o resultado da operação
  ///
  @override
  Future<Either<Exception, AuthModel>> get<AuthModel>({required int id}) async {
    try {
      return Right(authModel as AuthModel);
    } catch (error, stackTrace) {
      AppLogger().erro('Error getting item from database', error, stackTrace);
      return Left(Exception('Error getting item from database'));
    }
  }

  /// Método para inserir um item no banco de dados local
  ///
  /// Params:
  ///  [data] - AuthModel - Dados a serem inseridos
  ///
  /// Return:
  ///  Either<Exception, bool> - Retorna o resultado da operação
  ///
  @override
  Future<Either<Exception, bool>> insert<AuthModel>(AuthModel data) async {
    try {
      // Implementado a lógica para inserir o item no banco de dados local
      return const Right(true);
    } catch (error, stackTrace) {
      AppLogger().erro('Error inserting item into database', error, stackTrace);
      return Left(Exception('Error inserting item into database'));
    }
  }
}
