
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Bridges your future BLoCs with [GoRouter]'s [refreshListenable].
class RouterNotifier extends ChangeNotifier {
  // TODO: Inject your AppBloc or AuthBloc here once created.
  // final AppBloc _appBloc;
  // late final StreamSubscription _blocSubscription;

  RouterNotifier() {
    // _blocSubscription = _appBloc.stream.listen((state) {
    //   notifyListeners();
    // });
  }

  @override
  void dispose() {
    // _blocSubscription.cancel();
    super.dispose();
  }

  /// Centralized redirect logic evaluated on every route change or state emission.
  String? redirect(BuildContext context, GoRouterState state) {
    // Future logic:
    // final hasCompletedOnboarding = _appBloc.state.hasCompletedOnboarding;
    // final isAuthenticated = _appBloc.state.isAuthenticated;

    // For now, since we only have onboarding, we do not redirect.
    return null;
  }
}
