///
/// [Arquivo gerado automatimante pelo NuvolsCore]
///
/// [Travado por default]
/// Por ser um arquivo de configuração, para evitar que o mesmo seja sobrescrito
/// por um novo build do Core, o mesmo está travado por default.
/// #FileLocked
///
library;

import 'package:flutter/foundation.dart';

const bool developingAtHome = true;
const String homeIPAddress = 'http://192.168.68.106';
const String workIPAddress = 'http://192.168.1.140';

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
const String uriRelease = 'http://45.178.182.27:8000/';
const String uriFastAPIRelease = 'http://45.178.182.27:8001/';

// URL para os termos de uso
const String urlTermoUso = '';

// Área para configuração das modalidades de registro e login
const bool enabledFacebookAccount = false;
const bool enabledGoogleAccount = false;
const bool enabledEmailAccount = false;
const bool enabledOTPAccount = false;

// ///
// /// [getFastAPIPasswordRemoteConfig]
// ///
// /// Método para retornar a senha da camada FastAPI baseado no debugMode
// /// caso esteja em desenvolvimento retorna a senha padrão, caso contrário
// /// vai buscar a senha no Firebase Remote Config
// ///
// /// [Return]:
// ///  String - Senha da camada FastAPI
// ///
// Future<String> getFastAPIPasswordRemoteConfig() async {
//   try {
//     if (releaseVersion == false) {
//       return Config.fastAPIPasswordDevelopment;
//     }
//     final String? config = await ApplicationConfig.getFirebaseRemoteConfig('mvaMfN2DWmXD9g1P_default_password_fastapi');
//     if (config != null) {
//       return config;
//     }
//     return '';
//   } catch (error, stackTrace) {
//     NuvolsCoreLogger().erro('Erro ao chamar o getFAstAPIPasswordRemoteConfig', error, stackTrace);
//     return '';
//   }
// }

// ///
// /// [getFastAPIAuthUserRemoteConfig]
// ///
// /// Método para retornar o usuário da camada FastAPI baseado no debugMode
// /// caso esteja em desenvolvimento retorna o usuário padrão, caso contrário
// /// vai buscar o usuário no Firebase Remote Config
// ///
// /// [Return]:
// ///  String - Usuário da camada FastAPI
// ///
// Future<String> getFastAPIAuthUserRemoteConfig() async {
//   try {
//     if (releaseVersion == false) {
//       return Config.fastAPIUserDevelopment;
//     }
//     final String? config = await ApplicationConfig.getFirebaseRemoteConfig('userauth_fastapi_layer');
//     if (config != null) {
//       return config;
//     }
//     return '';
//   } catch (error, stackTrace) {
//     NuvolsCoreLogger().erro('Erro ao chamar o getFastAPIAuthUserRemoteConfig', error, stackTrace);
//     return '';
//   }
// }

// ///
// /// [getFastAPIURIRemoteConfig]
// ///
// /// Método para retornar a URI da camanda FastAPI baseado no debugMode
// /// caso esteja em desenvolvimento retorna o localhost, caso contrário
// /// vai buscar a URI no Firebase Remote Config
// ///
// /// [Return]:
// ///  String - URI da camada FastAPI
// ///
// Future<String> getFastAPIURIRemoteConfig() async {
//   try {
//     if (releaseVersion == false) {
//       return Config.fastAPIURI;
//     }
//     final String? config = await ApplicationConfig.getFirebaseRemoteConfig('uri_api_fastapi');
//     if (config != null) {
//       return config;
//     }
//     return '';
//   } catch (error, stackTrace) {
//     NuvolsCoreLogger().erro('Erro ao chamar o getFastAPIURIRemoteConfig', error, stackTrace);
//     return '';
//   }
// }

class Config {
  static const uri = releaseVersion ? uriRelease : uriDeveloper;
  static const uriAuth = '';

  // Adicionar aqui o token DRF caso esteja utilizando o Django Rest Framework.
  static const drfToken = 'Token db88e83b3eebe7e0ebd925cc6ae7ed21afc8684e';

  // Dados da camada FastAPI
  static const fastAPIUserDevelopment = 'email@email.com';
  static const fastAPIPasswordDevelopment = 'asdf@1234';
  static const fastAPIURI = releaseVersion ? uriFastAPIRelease : fastAPIURIDeveloper;

  static const String uriMedia = 'media/';
  static const String appTitle = '40x40';
  static const bool usingURL = false;
  static const double marginHead = 0.25;

  // Método GET para retornar o path completo do Media
  static String get getMediaPath => uri;
}

// // Área de definição das classes que encapsulam as String defaultas
// // das telas de listagem, inserção, edição, exclusão e detalhamento
// class DefaultProccessStringConstants {
//   static const String loading = 'Processando...';
//   static const String error = 'Erro ao executar a operação';
//   static const String success = 'Operação realizada com sucesso';
//   static const String empty = 'Nenhum registro encontrado';
// }

// class ListStringConstants {
//   static const String loading = 'Carregando...';
//   static const String error = 'Erro ao carregar os dados';
//   static const String refreshError = 'Erro ao recarregar os dados';
//   static const String loadingError = 'Erro ao carregar os dados';
//   static const String success = 'Dados carregados com sucesso';
//   static const String empty = 'Nenhum registro encontrado';
// }

// class DetailStringConstants {
//   static const String loading = 'Detalhando...';
//   static const String loadingError = 'Erro ao carregar os dados';
//   static const String error = 'Erro ao detalhar o item';
//   static const String success = 'Item detalhado com sucesso';
//   static const String empty = 'Item não encontrado';
// }

// class InsertStringConstants {
//   static const String loading = 'Cadastrando...';
//   static const String loadingError = 'Erro ao carregar os dados';
//   static const String error = 'Erro ao cadastrar o item';
//   static const String success = 'Item cadastrado com sucesso';
//   static const String empty = '';
// }

// class UpdateStringConstants {
//   static const String loading = 'Atualizando...';
//   static const String loadingError = 'Erro ao carregar os dados';
//   static const String error = 'Erro ao atualizar o item';
//   static const String success = 'Item atualizado com sucesso';
//   static const String empty = '';
// }

// /// [==================================================================]
// /// [                 Área para configurações do Figma                  ]
// /// [==================================================================]

// class ConnectaTheme {
//   static Color defaultColor = Colors.black;

//   static Color lightPrimary = const Color(0xFF00639C);
//   static Color lightAccent = const Color(0xFF715C00);
//   static Color lightBG = const Color(0xFFF8FDFF);
//   static Color backgroundPageLight = const Color(0xFFF8FDFF);
//   static Color lightCardColor = const Color.fromARGB(255, 255, 255, 255);
//   static Color lightErrorColor = const Color(0xFFBA1A1A);
//   static Color lightTextColor = const Color.fromARGB(255, 108, 174, 224);
//   static Color lightTextButtonLabelColor = const Color.fromARGB(255, 236, 232, 232);
//   static Color lightTextButtonColor = const Color.fromARGB(255, 41, 138, 218);
//   static Color lightTextColorTextFormField = const Color(0xFF4a5c6a);
//   static Color lightConnectaIconMenuHome = const Color(0xFF678CBD);
//   static Color lightConnectaCardHead = Colors.white;
//   static Color lightTextColorConnectaCardHead = const Color(0xFF514766);
//   static Color lightSubTitleColorConnectaCardHead = const Color(0xFF514766);

//   static Color darkPrimary = Colors.black;
//   static Color darkAccent = const Color.fromARGB(255, 126, 127, 130);
//   static Color darkBG = const Color.fromARGB(255, 37, 39, 41);
//   static Color backgroundPageDark = const Color.fromARGB(255, 56, 54, 54);
//   // static Color darkBG = const Color.fromARGB(255, 57, 29, 29); // Cor proposta pelo cliente
//   static Color darkCardColor = const Color.fromARGB(255, 126, 127, 130);
//   static Color darkErrorColor = const Color(0xFFBA1A1A);
//   static Color darkTextColor = const Color.fromARGB(255, 203, 208, 212);
//   static Color darkTextButtonLabelColor = const Color.fromARGB(255, 253, 253, 253);
//   static Color darkTextButtonColor = const Color.fromARGB(255, 147, 186, 218);
//   static Color darkTextButtonOrangeColor = Colors.orangeAccent;
//   static Color darkTextColorTextFormField = const Color(0xFF4a5c6a);
//   static Color darkConnectaIconMenuHome = const Color.fromARGB(255, 150, 189, 239);
//   static Color darkConnectaCardHead = Colors.grey.shade800;
//   static Color darkTextColorConnectaCardHead = const Color.fromARGB(255, 202, 189, 231);
//   static Color darkSubTitleColorConnectaCardHead = const Color.fromARGB(255, 175, 154, 221);

//   static Color textStyleDefaultColor = const Color(0xFF4a5c6a);

//   static String fontFamily = 'Inter';

//   static ThemeData light = ThemeData(
//     primaryColor: lightPrimary,
//     secondaryHeaderColor: lightBG,
//     unselectedWidgetColor: lightConnectaCardHead, // Cor do ConnectaCardHead
//     scaffoldBackgroundColor: backgroundPageLight,
//     cardColor: lightCardColor,
//     highlightColor: lightConnectaIconMenuHome, // Cor para os ícones do menu
//     textTheme: TextTheme(
//       displayLarge: TextStyle(
//         color: lightPrimary,
//         fontFamily: fontFamily,
//       ),
//       displayMedium: TextStyle(
//         color: lightPrimary,
//         fontFamily: fontFamily,
//       ),
//       displaySmall: TextStyle(
//         // Text Padrão utilizado para os subTitulos do ConnectaCardHead
//         color: lightSubTitleColorConnectaCardHead,
//         fontSize: 12,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w400,
//       ),
//       headlineLarge: TextStyle(
//         color: lightPrimary,
//         fontFamily: fontFamily,
//       ),
//       headlineMedium: TextStyle(
//         // Text padrão para o texto 'Legenda'
//         color: lightPrimary,
//         fontFamily: fontFamily,
//         fontSize: 14,
//       ),
//       headlineSmall: TextStyle(
//         // Text Padrão utilizado para os textos do ConnectaCardHead
//         color: lightTextColorConnectaCardHead,
//         fontSize: 20,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w700,
//       ),
//       titleLarge: TextStyle(
//         // Text Padrão utilizado para os títulos (head das telas)
//         color: lightTextColor,
//         fontSize: 20,
//         fontWeight: FontWeight.w600,
//         fontFamily: fontFamily,
//       ),
//       titleMedium: TextStyle(
//         // Text Padrão para os textos dos TextFormFields
//         color: lightTextColorTextFormField,
//         fontFamily: fontFamily,
//         fontSize: 14,
//       ),
//       titleSmall: TextStyle(
//         // Text padrão para ser utilizado nos botões do tipo text
//         color: lightTextButtonColor,
//         fontSize: 12,
//         fontWeight: FontWeight.w300,
//         fontFamily: 'Poppins',
//       ),
//       bodyLarge: TextStyle(
//         color: Colors.black,
//         fontFamily: fontFamily,
//       ),
//       bodyMedium: const TextStyle(
//         // Text padrão para os textos de estatísticas
//         color: Colors.black,
//         fontFamily: 'Popins',
//         fontSize: 18,
//         fontWeight: FontWeight.w600,
//       ),
//       bodySmall: const TextStyle(
//         fontSize: 18,
//         height: 1.10,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w500,
//         color: Color(0xFF514766),
//       ),
//       labelLarge: const TextStyle(
//         // Text para ser utilizado no texto superior direito dos ConnectaCardMenuItemHome
//         color: Color(0xFFD6D6DD),
//         fontFamily: 'Offside',
//         fontSize: 24,
//         fontWeight: FontWeight.w500,
//       ),
//       labelMedium: TextStyle(
//         // Text Padrão utilizado para os botões
//         color: lightTextColor,
//         fontFamily: fontFamily,
//         fontSize: 20,
//       ),
//       labelSmall: TextStyle(
//         color: Colors.black45,
//         fontFamily: fontFamily,
//         fontSize: 12,
//       ),
//     ),
//     elevatedButtonTheme: ElevatedButtonThemeData(
//       style: ButtonStyle(
//         backgroundColor: MaterialStateProperty.all(lightPrimary),
//         foregroundColor: MaterialStateProperty.all(lightTextButtonLabelColor),
//         shape: MaterialStateProperty.all<RoundedRectangleBorder>(
//           RoundedRectangleBorder(
//             borderRadius: BorderRadius.circular(50),
//           ),
//         ),
//         padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
//           const EdgeInsets.symmetric(vertical: 5),
//         ),
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: lightTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     outlinedButtonTheme: OutlinedButtonThemeData(
//       style: ButtonStyle(
//         backgroundColor: MaterialStateProperty.all(lightPrimary),
//         foregroundColor: MaterialStateProperty.all(lightTextButtonLabelColor),
//         shape: MaterialStateProperty.all<RoundedRectangleBorder>(
//           RoundedRectangleBorder(
//             borderRadius: BorderRadius.circular(50),
//           ),
//         ),
//         padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
//           const EdgeInsets.symmetric(vertical: 5),
//         ),
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: lightTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     textButtonTheme: TextButtonThemeData(
//       style: ButtonStyle(
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: lightTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     appBarTheme: AppBarTheme(
//       elevation: 0,
//       backgroundColor: backgroundPageLight,
//       toolbarTextStyle: TextTheme(
//         titleMedium: TextStyle(
//           color: lightBG,
//           fontSize: 18.0,
//           fontWeight: FontWeight.w800,
//         ),
//       ).bodyMedium,
//       titleTextStyle: TextTheme(
//         titleMedium: TextStyle(
//           color: lightBG,
//           fontSize: 18.0,
//           fontWeight: FontWeight.w800,
//         ),
//       ).titleLarge,
//     ),
//     colorScheme: ColorScheme.fromSwatch(brightness: Brightness.light)
//         .copyWith(
//           secondary: lightAccent,
//         )
//         .copyWith(
//           background: lightBG,
//         ),
//   );
//   static ThemeData dark = ThemeData(
//     primaryColor: darkPrimary,
//     secondaryHeaderColor: darkAccent,
//     scaffoldBackgroundColor: darkBG,
//     unselectedWidgetColor: darkConnectaCardHead, // Cor do ConnectaCardHead
//     cardColor: darkCardColor,
//     highlightColor: darkConnectaIconMenuHome, // Cor para os ícones do menu
//     textTheme: TextTheme(
//       displayLarge: TextStyle(
//         color: darkPrimary,
//       ),
//       displayMedium: TextStyle(
//         color: darkPrimary,
//       ),
//       displaySmall: TextStyle(
//         // Text Padrão utilizado para os subTitulos do ConnectaCardHead
//         color: darkSubTitleColorConnectaCardHead,
//         fontSize: 12,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w400,
//       ),
//       headlineLarge: TextStyle(
//         color: darkPrimary,
//       ),
//       headlineMedium: TextStyle(
//         // Text padrão para o texto 'Legenda'
//         color: Colors.white,
//         fontFamily: fontFamily,
//         fontSize: 14,
//       ),
//       headlineSmall: TextStyle(
//         // Text Padrão utilizado para os textos do ConnectaCardHead
//         color: darkTextColorConnectaCardHead,
//         fontSize: 20,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w700,
//       ),
//       titleLarge: TextStyle(
//         // Text Padrão utilizado para os títulos (head das telas)
//         color: darkTextColor,
//         fontSize: 20,
//         fontWeight: FontWeight.w600,
//         fontFamily: fontFamily,
//       ),
//       titleMedium: TextStyle(
//         // Text Padrão para os textos dos TextFormFields
//         color: lightTextColorTextFormField,
//         fontFamily: fontFamily,
//         fontSize: 14,
//       ),
//       titleSmall: TextStyle(
//         // Text padrão para ser utilizado nos botões do tipo text
//         color: darkTextButtonOrangeColor,
//         fontSize: 12,
//         fontWeight: FontWeight.w300,
//         fontFamily: 'Poppins',
//       ),
//       bodyLarge: const TextStyle(
//         color: Colors.white,
//       ),
//       bodyMedium: const TextStyle(
//         // Text padrão para os textos de estatísticas
//         color: Colors.white,
//         fontFamily: 'Popins',
//         fontSize: 18,
//         fontWeight: FontWeight.w600,
//       ),
//       bodySmall: const TextStyle(
//         fontSize: 18,
//         height: 1.10,
//         fontFamily: 'Poppins',
//         fontWeight: FontWeight.w500,
//         color: Color.fromARGB(255, 206, 190, 241),
//       ),
//       labelLarge: const TextStyle(
//         // Text para ser utilizado no texto superior direito dos ConnectaCardMenuItemHome
//         color: Color(0xFFD6D6DD),
//         fontFamily: 'Offside',
//         fontSize: 24,
//         fontWeight: FontWeight.w500,
//       ),
//       labelMedium: TextStyle(
//         // Text Padrão utilizado para os botões
//         color: Colors.white,
//         fontFamily: fontFamily,
//         fontSize: 20,
//       ),
//       labelSmall: TextStyle(
//         fontFamily: fontFamily,
//         color: Colors.white,
//         fontSize: 12,
//       ),
//     ),
//     elevatedButtonTheme: ElevatedButtonThemeData(
//       style: ButtonStyle(
//         backgroundColor: MaterialStateProperty.all(Colors.orangeAccent),
//         foregroundColor: MaterialStateProperty.all(darkTextButtonLabelColor),
//         shape: MaterialStateProperty.all<RoundedRectangleBorder>(
//           RoundedRectangleBorder(
//             borderRadius: BorderRadius.circular(50),
//           ),
//         ),
//         padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
//           const EdgeInsets.symmetric(vertical: 5),
//         ),
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: darkTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     outlinedButtonTheme: OutlinedButtonThemeData(
//       style: ButtonStyle(
//         foregroundColor: MaterialStateProperty.all(darkTextButtonLabelColor),
//         shape: MaterialStateProperty.all<RoundedRectangleBorder>(
//           RoundedRectangleBorder(
//             borderRadius: BorderRadius.circular(50),
//           ),
//         ),
//         padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
//           const EdgeInsets.symmetric(vertical: 5),
//         ),
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: darkTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     textButtonTheme: TextButtonThemeData(
//       style: ButtonStyle(
//         textStyle: MaterialStateProperty.all<TextStyle>(
//           TextStyle(
//             color: darkTextButtonLabelColor,
//             fontFamily: 'Poppins',
//             fontSize: 20,
//           ),
//         ),
//       ),
//     ),
//     appBarTheme: AppBarTheme(
//       elevation: 0,
//       toolbarTextStyle: TextTheme(
//         titleMedium: TextStyle(
//           color: darkBG,
//           fontSize: 18.0,
//           fontWeight: FontWeight.w800,
//         ),
//       ).bodyMedium,
//       titleTextStyle: TextTheme(
//         titleMedium: TextStyle(
//           color: darkBG,
//           fontSize: 18.0,
//           fontWeight: FontWeight.w800,
//         ),
//       ).titleLarge,
//     ),
//     colorScheme: ColorScheme.fromSwatch(brightness: Brightness.dark)
//         .copyWith(
//           secondary: darkAccent,
//         )
//         .copyWith(
//           background: darkBG,
//         ),
//   );
// }
