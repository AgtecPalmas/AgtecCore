import 'package:flutter/material.dart';

import '../../constants/app.sizes.dart';

class AppEmptyList extends StatelessWidget {
  const AppEmptyList({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: MediaQuery.sizeOf(context).height * AppSizeMarginPadding.heightSizedBoxParentTable,
      child: Center(child: Text('Nenhum item encontrado')),
    );
  }
}
