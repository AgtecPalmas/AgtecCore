///
/// Controller responsável por gerenciar o dashboard do aplicativo.
///
/// Métodos:
///  -- getContasAPagar() -> Recupera a lista de contas a pagar.
///  -- getAniversariantes() -> Recupera a lista de aniversariantes.
///  -- getContasAReceber() -> Recupera a lista de contas a receber.

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';


part '../states/dashboard.dart';

class DashboardController extends Cubit<DashboardState> {
  DashboardController() : super(DashboardInitial());

}
