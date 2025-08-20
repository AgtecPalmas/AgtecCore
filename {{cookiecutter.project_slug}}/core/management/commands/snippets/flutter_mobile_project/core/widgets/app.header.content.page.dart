// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '/constants/app.colors.dart';

import '/core/styles/app.text.style.dart';

class AppHeaderPage extends StatefulWidget {
  final String title;
  final bool searchEnabled;
  final String previusRoute;
  const AppHeaderPage({super.key, required this.title, this.searchEnabled = false, this.previusRoute = ''});

  @override
  State<AppHeaderPage> createState() => _AppHeaderPageState();
}

class _AppHeaderPageState extends State<AppHeaderPage> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          if (widget.previusRoute.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.arrow_back_ios_new, color: AppColors.blue222222),
              onPressed: () {
                context.go(widget.previusRoute);
              },
            ),
          Text(widget.title, style: AppTextTitlePageStyle.style()),
        ],
      ),
    );
  }

}
