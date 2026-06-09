import 'package:either_dart/either.dart';
import '/core/app.config.dart';
import '/core/app.dependencies.injection.dart';
import '/core/dio/app_dio.dart';
import '/core/interfaces/http.dart';

class DashboardService implements HttpInterface {
  final String _uri = '${Config.uri}/api/v1/dashboard/dashboard/';

  // Recuperando o Dio pelo getIt
  final AppDio _dio = getIt<AppDio>();

  @override
  Future<Either<Exception, List<T>>> fetch<T>({String? uri, returnResult = false}) async {
    try {
      final response = await _dio.get(
        uri: uri ?? _uri,
        returnResult: returnResult,
      );
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error fetching data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error fetching data, error: $error'));
    }
  }

  @override
  Future<Either<Exception, List<T>>> getMore<T>({required String uri, returnResult = false}) async {
    try {
      final response = await _dio.get(
        uri: uri,
        returnResult: returnResult,
      );
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error fetching data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error fetching data, error: $error'));
    }
  }

  @override
  Future<Either<Exception, T>> detail<T>({String? uri, required String id}) async {
    try {
      String url = uri ?? _uri;
      url += id;
      final response = await _dio.get(uri: url, returnResult: true);
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error fetching data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error fetching data, error: $error'));
    }
  }

  @override
  Future<Either<Exception, T>> post<T>({
    String? uri,
    data,
    bool multipart = false,
  }) async {
    try {
      final response = await _dio.post(
        uri: uri ?? _uri,
        data: data,
        multipart: multipart,
      );
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error posting data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error posting data, error: $error'));
    }
  }

  @override
  Future<Either<Exception, T>> put<T>({
    required dynamic data,
    bool multipart = false,
  }) async {
    try {
      final response = await _dio.put(
        uri: _uri,
        data: data,
        multipart: multipart,
      );
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error updating data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error updating data, error: $error'));
    }
  }
  
  @override
  Future<Either<Exception, T>> patch<T>({
    required dynamic data,
    bool multipart = false,
  }) async {
    try {
      final response = await _dio.patch(
        uri: _uri, data: data,
        multipart: multipart,
      );
      if (response.isRight) {
        return Right(response.right);
      }
      return Left(Exception('Error patching data, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error patching data, error: $error'));
    }
  }

  @override
  Future<Either<Exception, bool>> delete({required String id}) async {
    try {
      final response = await _dio.delete(
        uri: _uri,
        id: id,
      );
      if (response.isRight) {
        return const Right(true);
      }
      return Left(Exception('Error deleting item, error: ${response.left}'));
    } catch (error) {
      return Left(Exception('Error deleting item, error: $error'));
    }
  }
}
