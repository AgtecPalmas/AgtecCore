import 'package:flutter/material.dart';

class SigInPage extends StatefulWidget {
  const SigInPage({super.key, required this.title});
  final String title;

  @override
  State<SigInPage> createState() => _SigInPageState();
}

class _SigInPageState extends State<SigInPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(body: _buildContent());
  }

  ///
  /// [_buildContent]
  /// Método para criar o build
  ///
  Widget _buildContent() {
    return CustomScrollView(slivers: [SliverFillRemaining(child: Container())]);
  }
}
