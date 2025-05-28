import 'package:flutter/material.dart';

class AppBarPage extends StatelessWidget {
  final String title;
  const AppBarPage({super.key, this.title = 'App'});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(radius: 16, backgroundImage: NetworkImage('https://example.com/profile.jpg')),
        SizedBox(width: 8),
        Expanded(child: Text(title, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold))),
        IconButton(
          icon: const Icon(Icons.settings),
          onPressed: () {
            // Action for settings button
          },
        ),
      ],
    );
  }
}
