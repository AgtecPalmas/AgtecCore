import 'dart:async';

import 'package:flutter/foundation.dart';

class AppDebouncer {
  final int milliseconds;
  Timer? _timer;

  AppDebouncer({required this.milliseconds});

  void call(VoidCallback callback) {
    _timer?.cancel();
    _timer = Timer(Duration(milliseconds: milliseconds), callback);
  }
}
