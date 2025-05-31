///
/// [Arquivo gerado automaticamente pelo NuvolsCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração, para evitar que o mesmo seja sobrescrito
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///
///

import 'package:flutter/foundation.dart';

const bool developingAtHome = true;
const String homeIPAddress = 'http://192.168.68.110';
const String workIPAddress = 'http://11.11.0.112';

// Área para nome de constantes que servirão de chave para os dados
const accessTokenDRF = 'accessTokenDRF';
const refreshTokenDRF = 'refreshTokenDRF';
const accessTokenFastAPI = 'accessTokenFastAPI';
const refreshTokenFastAPI = 'refreshTokenFastAPI';
const arenaManagementID = 'arenaManagementID';

// Chave para determinar se a versão está em desenvolvimento ou produção
// Para executar localmente e apontar para o banco de produção
// deve ficar releaseVersion = kDebugMode

// Para enviar para produção deve ficar releaseVersion = !kDebugMode
const bool releaseVersion = !kDebugMode;

// URI para desenvolvimento
const String uriDeveloper = developingAtHome ? '$homeIPAddress:8000/' : '$workIPAddress:8000/';
const String fastAPIURIDeveloper = developingAtHome ? '$homeIPAddress:8181/' : '$workIPAddress:8181/'; // Prefeitura

// URI para produção
const String uriRelease = '';
const String uriFastAPIRelease = '';

// URL para os termos de uso
const String urlTermoUso = '';

// Área para configuração das modalidades de registro e login
const bool enabledFacebookAccount = false;
const bool enabledGoogleAccount = false;
const bool enabledEmailAccount = false;
const bool enabledOTPAccount = false;


class Config {
  static const uri = releaseVersion ? fastAPIURIDeveloper : fastAPIURIDeveloper;
  static const uriAuth = '';

  // Adicionar aqui o token DRF caso esteja utilizando o Django Rest Framework.
  static const drfToken = 'Token ';

  // Dados da camada FastAPI
  static const fastAPIUserDevelopment = 'email@email.com';
  static const fastAPIPasswordDevelopment = 'asdf@1234';
  static const fastAPIURI = releaseVersion ? uriFastAPIRelease : fastAPIURIDeveloper;

  static const String uriMedia = 'media/';
  static const String appTitle = 'App';
  static const bool usingURL = false;
  static const double marginHead = 0.25;

  // Método GET para retornar o path completo do Media
  static String get getMediaPath => uri;
}
