import 'package:flutter/material.dart';

import '../../constants/app.colors.dart';

class AppBottomBar extends StatefulWidget {
  final List<Widget> itens;

  const AppBottomBar({super.key, required this.itens});

  @override
  State<AppBottomBar> createState() => _AppBottomBarState();
}

class _AppBottomBarState extends State<AppBottomBar> {
  @override
  Widget build(BuildContext context) {
    return Positioned(
      bottom: 0,
      child: Container(
        height: 62,
        width: MediaQuery.of(context).size.width * .95,
        decoration: const BoxDecoration(
          color: AppColors.bigStoneBlue,
          borderRadius: BorderRadius.only(
            bottomLeft: Radius.circular(20),
            bottomRight: Radius.circular(20),
            topLeft: Radius.circular(20),
            topRight: Radius.circular(20),
          ),
        ),
        margin: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          mainAxisSize: MainAxisSize.max,
          children: [...widget.itens],
        ),
      ),
    );
  }
}
