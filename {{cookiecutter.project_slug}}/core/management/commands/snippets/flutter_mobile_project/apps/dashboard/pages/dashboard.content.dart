import 'package:flutter/material.dart';

import '../../../core/widgets/app.appbar.dart';
import '../../../core/widgets/app.menudashboard.dart';

class DashboardContent extends StatefulWidget {
  const DashboardContent({super.key});

  @override
  State<DashboardContent> createState() => _DashboardContentState();
}

class _DashboardContentState extends State<DashboardContent> {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          AppBarPage(),
          const SizedBox(height: 20),
          Text('Módulos', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          // GridView com três colunas para mostrar o acesso aos módulos
          Expanded(
            child: GridView.count(
              crossAxisCount: 4,
              crossAxisSpacing: 8,
              mainAxisSpacing: 8,
              children: [
                $MenuItensDashboard$
              ],
            ),
          ),
        ],
      ),
    );
  }
}
