
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// Assuming this is your exact path
import 'package:fin_front/src/features/onboarding/presentation/pages/onboarding_page.dart';
import 'router_notifier.dart';

class AppRouter {
  late final RouterNotifier _routerNotifier;
  late final GoRouter router;

  AppRouter() {
    _routerNotifier = RouterNotifier();

    router = GoRouter(
      refreshListenable: _routerNotifier,
      redirect: _routerNotifier.redirect,
      initialLocation: '/',
      // Strict mode for deep linking (prevents URL spoofing in web/deep links)
      routerNeglect: false,
      routes: [
        GoRoute(
          path: '/',
          name: 'onboarding',
          // ALWAYS use const for O(1) widget building where possible
          builder: (context, state) => const OnboardingPage(),
        ),
      ],
      // Catch-all functional error handling for invalid routes
      errorBuilder: (context, state) => Scaffold(
        body: Center(child: Text('Routing Error: ${state.error}')),
      ),
    );
  }

  /// Call this when the app terminates or if resetting the DI container
  void dispose() {
    _routerNotifier.dispose();
  }
}
