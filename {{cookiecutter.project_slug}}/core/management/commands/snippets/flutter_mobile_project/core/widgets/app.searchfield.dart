import 'package:flutter/material.dart';

import '../styles/app.formfield.style.dart';

class AppSearchfieldListViewPage<T> extends StatefulWidget {
  final String? labelText;
  const AppSearchfieldListViewPage({super.key, labelText}) : labelText = labelText ?? 'Pesquisar/filtrar';

  @override
  State<AppSearchfieldListViewPage> createState() => _AppSearchfieldListViewPageState();
}

class _AppSearchfieldListViewPageState extends State<AppSearchfieldListViewPage> {
  String searchText = '';

  @override
  Widget build(BuildContext context) {
    return TextFormField(decoration: AppSearchFieldStyle.style());
  }
}
