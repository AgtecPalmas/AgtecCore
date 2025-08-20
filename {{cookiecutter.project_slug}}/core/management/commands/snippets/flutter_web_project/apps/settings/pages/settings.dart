import 'package:flutter/material.dart';
import '/apps/settings/pages/content.dart';
import '/constants/app.colors.dart';
import '/core/widgets/app.menu.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key, required this.title});
  final String title;

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return const Material(
      color: AppColors.desktopBackground,
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Row(
          children: [
            AppMenuToolbar(
              currentPath: 'settings',
            ),
            Expanded(
              child: ContentSettingPage(),
            ),
          ],
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
