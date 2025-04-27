import '/core/app.logger.dart';

class AuthModel {
  String id = '';
  String uuid = '';
  String name = '';
  String email = '';
  String login = '';
  String socialProfileLogin = '';
  String account = '';
  String password = '';
  String cpf = '';
  String phoneNumber = '';
  String photoUrl = '';
  String token = '';
  String firebaseId = '';
  String firebaseToken = '';
  String accessToken = '';
  String refreshToken = '';
  String idToken = '';
  String fastAPIAccessToken = '';
  String fastAPIRefreshToken = '';

  AuthModel({
    this.id = '',
    this.uuid = '',
    this.name = '',
    this.email = '',
    this.login = '',
    this.socialProfileLogin = '',
    this.account = '',
    this.password = '',
    this.cpf = '',
    this.phoneNumber = '',
    this.token = '',
    this.photoUrl = '',
    this.firebaseId = '',
    this.accessToken = '',
    this.refreshToken = '',
    this.idToken = '',
    this.firebaseToken = '',
    this.fastAPIAccessToken = '',
    this.fastAPIRefreshToken = '',
  });

/// Construtor nomeado que retorna uma instância com todos os atributos vazios
  factory AuthModel.empty() {
    return AuthModel(
      id: '',
      uuid: '',
      name: '',
      email: '',
      login: '',
      socialProfileLogin: '',
      account: '',
      password: '',
      cpf: '',
      phoneNumber: '',
      photoUrl: '',
      token: '',
      firebaseId: '',
      firebaseToken: '',
      accessToken: '',
      refreshToken: '',
      idToken: '',
      fastAPIAccessToken: '',
      fastAPIRefreshToken: '',
    );
  }

  String get profileName {
    try {
      if (account.isEmpty) return '';
      return account;
    } catch (error, stackTrace) {
      NuvolsCoreLogger().erro('Ocorreu o erro no AuthModel profileName', error, stackTrace);
    }
    return '';
  }

  @override
  String toString() {
    return 'AuthModel{id: $id, uuid: $uuid, name: $name, email: $email, login: $login, socialProfileLogin: $socialProfileLogin, account: $account, password: $password, cpf: $cpf, token: $token}';
  }

  factory AuthModel.fromMap(Map<String, dynamic> map) {
    try {
      return AuthModel(
        id: map.containsKey('id') ? map['id'] as String : '',
        uuid: map.containsKey('uuid') ? map['uuid'] as String : '',
        name: map.containsKey('name') ? map['name'] as String : '',
        email: map.containsKey('email') ? map['email'] as String : '',
        login: map.containsKey('login') ? map['login'] as String : '',
        socialProfileLogin: map.containsKey('socialProfileLogin') ? map['socialProfileLogin'] as String : '',
        account: map.containsKey('account') ? map['account'] as String : '',
        password: map.containsKey('password') ? map['password'] as String : '',
        cpf: map.containsKey('cpf') ? map['cpf'] as String : '',
        phoneNumber: map.containsKey('phoneNumber') ? map['phoneNumber'] as String : '',
        photoUrl: map.containsKey('photoUrl') ? map['photoUrl'] as String : '',
        token: map.containsKey('token') ? map['token'] as String : '',
        firebaseId: map.containsKey('firebaseId') ? map['firebaseId'] as String : '',
        firebaseToken: map.containsKey('firebaseToken') ? map['firebaseToken'] as String : '',
        accessToken: map.containsKey('accessToken') ? map['accessToken'] as String : '',
        refreshToken: map.containsKey('refreshToken') ? map['refreshToken'] as String : '',
        idToken: map.containsKey('idToken') ? map['idToken'] as String : '',
        fastAPIAccessToken: map.containsKey('fastAPIAccessToken') ? map['fastAPIAccessToken'] as String : '',
        fastAPIRefreshToken: map.containsKey('fastAPIRefreshToken') ? map['fastAPIRefreshToken'] as String : '',
      );
    } catch (error, stackTrace) {
      NuvolsCoreLogger().erro('Ocorreu o erro no AuthModel fromMap', error, stackTrace);
      return AuthModel();
    }
  }

  Map<String, dynamic> toMap() {
    try {
      return {
        'id': id,
        'uuid': uuid,
        'name': name,
        'email': email,
        'login': login,
        'socialProfileLogin': socialProfileLogin,
        'account': account,
        'password': password,
        'cpf': cpf,
        'phoneNumber': phoneNumber,
        'photoUrl': photoUrl,
        'token': token,
        'firebaseId': firebaseId,
        'firebaseToken': firebaseToken,
        'accessToken': accessToken,
        'idToken': idToken,
        'refreshToken': refreshToken,
        'fastAPIAccessToken': fastAPIAccessToken,
        'fastAPIRefreshToken': fastAPIRefreshToken,
      };
    } catch (error, stackTrace) {
      NuvolsCoreLogger().erro('Ocorreu o erro no AuthModel toMap', error, stackTrace);
      return {};
    }
  }

  ///
  /// Método CopyWith
  ///
  AuthModel copyWith({
    String? id,
    String? uuid,
    String? name,
    String? email,
    String? login,
    String? socialProfileLogin,
    String? account,
    String? password,
    String? cpf,
    String? phoneNumber,
    String? photoUrl,
    String? token,
    String? firebaseId,
    String? firebaseToken,
    String? accessToken,
    String? refreshToken,
  }) {
    return AuthModel(
      id: id ?? this.id,
      uuid: uuid ?? this.uuid,
      name: name ?? this.name,
      email: email ?? this.email,
      login: login ?? this.login,
      socialProfileLogin: socialProfileLogin ?? this.socialProfileLogin,
      account: account ?? this.account,
      password: password ?? this.password,
      cpf: cpf ?? this.cpf,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      photoUrl: photoUrl ?? this.photoUrl,
      token: token ?? this.token,
      firebaseId: firebaseId ?? this.firebaseId,
      firebaseToken: firebaseToken ?? this.firebaseToken,
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
    );
  }

  /// [===============================================================]
  /// [===============================================================]
  /// [===================== Métodos Específicos ======================]
  /// [===============================================================]
  /// [===============================================================]
  ///
}
