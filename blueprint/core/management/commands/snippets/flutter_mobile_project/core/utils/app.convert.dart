import 'package:intl/intl.dart';

class AppConvertData {
  static DateTime? parseDataBrasileira(String dataTexto) {
    if (dataTexto.isEmpty) return null;

    try {
      // Remove caracteres não numéricos exceto /
      final dataLimpa = dataTexto.replaceAll(RegExp(r'[^0-9/]'), '');

      // Verifica se tem o formato correto (dd/MM/yyyy)
      if (dataLimpa.length == 10 && dataLimpa.split('/').length == 3) {
        return DateFormat('dd/MM/yyyy').parse(dataLimpa);
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
