import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

class AppMenuItem extends StatefulWidget {
  final String title;
  final String icon;
  final Function() onTap;
  final bool isSelected;

  const AppMenuItem({
    super.key,
    required this.title,
    required this.icon,
    required this.onTap,
    this.isSelected = false,
  });

  @override
  State<AppMenuItem> createState() => _AppMenuItemState();
}

class _AppMenuItemState extends State<AppMenuItem> {
  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: widget.onTap,
      child: Container(
        width: AppSizeMarginPadding.itemMenuW,
        height: AppSizeMarginPadding.itemMenuH,
        padding: const EdgeInsets.only(
            left: AppSizeMarginPadding.paddingMenuItemL,
            top: AppSizeMarginPadding.paddingMenuItemB,
            bottom: AppSizeMarginPadding.paddingMenuItemB),
        decoration: BoxDecoration(
          color: widget.isSelected ? AppColors.menuItemActivatedBackground : AppColors.transparent,
          borderRadius: const BorderRadius.all(
            Radius.circular(AppSizeMarginPadding.itemMenuSelectedRadius),
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset(
              'assets/icons/${widget.icon}',
              width: AppSizeMarginPadding.iconMenuDefaultWH,
              height: AppSizeMarginPadding.iconMenuDefaultWH,
              color: AppColors.menuIcon,
            ),
            const SizedBox(width: AppSizeMarginPadding.menuItemIconSpaceLabelH),
            Text(
              widget.title,
              style: AppMenuItemStyle.style(),
            ),
          ],
        ),
      ),
    );
  }
}
