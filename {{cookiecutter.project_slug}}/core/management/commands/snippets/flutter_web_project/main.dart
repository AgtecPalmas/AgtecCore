import 'package:flutter/material.dart';

import 'core/app.dependencies.injection.dart';
import 'core/app.routes.dart';



void main() {
  configureDependencies();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      routerConfig: appRouter,
    );
  }
}
