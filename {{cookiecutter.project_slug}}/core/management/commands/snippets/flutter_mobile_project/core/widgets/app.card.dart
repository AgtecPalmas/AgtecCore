// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';
import '/constants/app.colors.dart';
import '/constants/app.sizes.dart';
import '/core/styles/app.text.style.dart';

/// Classe padrão seguindo o DS da Nuvols
///
/// [Params]
///  - [cardContent] - Conteúdo do card
///  - [backgroundColor] - Cor de fundo do card
///
class AppCard extends StatelessWidget {
  final Widget cardContent;
  final String cardTitle;
  final Color? backgroundColor;
  final Color? borderColor;
  final double? borderWidth;
  final double borderRadius;
  final double? cardWidth;
  final double? cardHeight;

  const AppCard({
    super.key,
    required this.cardContent,
    required this.cardTitle,
    this.backgroundColor = AppColors.menuBackground,
    this.borderColor,
    this.borderWidth = AppSizeMarginPadding.borderCardW,
    this.borderRadius = AppSizeMarginPadding.cardRadiusDefault,
    this.cardWidth,
    this.cardHeight,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: cardWidth ?? double.infinity,
      margin: const EdgeInsets.only(
        top: AppSizeMarginPadding.marginDefaultTRBL,
      ),
      padding: const EdgeInsets.all(AppSizeMarginPadding.paddingDefaultTRBL),
      decoration: BoxDecoration(
        color: AppColors.menuBackground,
        borderRadius: BorderRadius.all(Radius.circular(
          borderRadius,
        )),
        border: Border.all(
          color: AppColors.cardBorder,
          width: AppSizeMarginPadding.borderCardW,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.max,
        children: [
          Text(
            cardTitle,
            style: AppTitleCardStyle.style(),
          ),
          const SizedBox(
            height: AppSizeMarginPadding.marginTitleCardTOSectionTitle,
          ),
          cardContent,
        ],
      ),
    );
  }
}
