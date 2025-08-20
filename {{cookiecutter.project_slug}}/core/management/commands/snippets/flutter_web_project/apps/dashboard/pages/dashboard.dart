import 'package:flutter/material.dart';

import '/constants/app.colors.dart';
import '/core/widgets/app.menu.dart';
import 'content.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key, required this.title});
  final String title;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  @override
  Widget build(BuildContext context) {
    return const Material(
      color: AppColors.desktopBackground,
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Row(children: [AppMenuToolbar(currentPath: 'dashboard'), Expanded(child: DashboardContent())]),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
