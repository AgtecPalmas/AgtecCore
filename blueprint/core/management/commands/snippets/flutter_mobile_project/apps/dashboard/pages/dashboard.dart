import 'package:flutter/material.dart';

import '../../../constants/app.colors.dart';
import 'dashboard.content.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key, required this.title});
  final String title;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(body: SafeArea(child: _buildContent()), backgroundColor: AppColors.backgroundScreen);
  }

  ///
  /// [_buildContent]
  /// Método para criar o build
  ///
  Widget _buildContent() {
    return CustomScrollView(slivers: [SliverFillRemaining(child: const DashboardContent())]);
  }
}
