import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

import '../../constants/app.colors.dart';
import '../../constants/app.sizes.dart';

class AppLoading extends StatelessWidget {
  final bool showTitle;
  const AppLoading({super.key, this.showTitle = true});

  @override
  Widget build(BuildContext context) {
    final spinkit = SpinKitWave(color: AppColors.bigStoneBlue, size: 50.0);
    return SizedBox(
      height: MediaQuery.sizeOf(context).height * AppSizeMarginPadding.heightSizedBoxParentTable,
      child: Column(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [spinkit, _buildTitle()],
      ),
    );
  }

  Widget _buildTitle() {
    if (!showTitle) {
      return const SizedBox.shrink();
    }
    return Column(children: [SizedBox(height: 22), Text('Carregando...', style: TextStyle(fontSize: 20))]);
  }
}
