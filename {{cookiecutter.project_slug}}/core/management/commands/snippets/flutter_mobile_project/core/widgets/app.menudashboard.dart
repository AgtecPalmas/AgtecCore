import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../constants/app.colors.dart';
import '../styles/app.text.style.dart';

class AppMenuItemDashboard extends StatefulWidget {
  final String title;
  final String icon;
  final String route;
  const AppMenuItemDashboard({super.key, required this.title, required this.icon, required this.route});

  @override
  State<AppMenuItemDashboard> createState() => _AppMenuItemDashboardState();
}

class _AppMenuItemDashboardState extends State<AppMenuItemDashboard> {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.push(widget.route);
      },
      child: Container(
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(8), color: AppColors.cardMenuDashboardBackground),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset('assets/icons/${widget.icon}', color: AppColors.cardMenuDashboardChildItens),
            const SizedBox(height: 8),
            Text(widget.title, style: AppMenuItemDashBoardStyle.style(),
            textAlign: TextAlign.center,),
          ],
        ),
      ),
    );
  }
}
