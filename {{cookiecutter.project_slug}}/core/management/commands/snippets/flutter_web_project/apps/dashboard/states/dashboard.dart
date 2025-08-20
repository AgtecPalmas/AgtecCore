part of '../controllers/dashboard.dart';

abstract class DashboardState extends Equatable {
  const DashboardState();
}

class DashboardInitial extends DashboardState {
  @override
  List<Object> get props => [];
}

class DashboardProccessState extends DashboardState {
  @override
  List<Object> get props => [];
}

class DashboardSuccessState extends DashboardState {
  final String successMessage;

  const DashboardSuccessState({
    required this.successMessage,
  });

  @override
  List<Object> get props => [successMessage,];
}

class DashboardErrorState extends DashboardState {
  final String error;

  const DashboardErrorState(this.error);

  @override
  List<Object> get props => [error];
}

class DashboardEmptyListState extends DashboardState {
  final String message;

  const DashboardEmptyListState(this.message);

  @override
  List<Object> get props => [message];
}
