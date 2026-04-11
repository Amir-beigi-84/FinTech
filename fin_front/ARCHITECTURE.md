# fin - Architecture

**State Management:** bloc
**Router:** go_router
**Profile:** full

## Features

- **splash_screen**
- **onboarding**
- **signinup**
- **financial_assessment**
- **first_setup_photo**
- **linking_bank**
- **home_screen**
- **transfer**
- **goal_saving**
- **qr_pay**
- **analytics**
- **profile**
- **subscription**
- **archive_goals**
- **settings**

## Clean Architecture Layers

### Domain Layer (Business Logic)
- **Entities**: Core business objects
- **Repositories**: Contracts/interfaces
- **Use Cases**: Application-specific business rules

### Data Layer (Implementation)
- **Models**: Data transfer objects
- **Data Sources**: Remote (API) and Local (DB/Cache)
- **Repository Implementations**: Concrete implementations

### Presentation Layer (UI)
- **Pages**: Screen layouts
- **Widgets**: Reusable UI components
- **State Management** (bloc): State holders

## Project Structure

```
lib/src/
├── core/
│   ├── constants/
│   ├── di/
│   ├── error/
│   ├── network/
│   ├── theme/
│   └── usecase/
├── features/
│   ├── splash_screen/
│   ├── onboarding/
│   ├── signinup/
│   ├── financial_assessment/
│   ├── first_setup_photo/
│   ├── linking_bank/
│   ├── home_screen/
│   ├── transfer/
│   ├── goal_saving/
│   ├── qr_pay/
│   ├── analytics/
│   ├── profile/
│   ├── subscription/
│   ├── archive_goals/
│   ├── settings/
├── app.dart
└── main.dart
```

## Next Steps

1. Implement entities in `domain/entities/`
2. Define repository contracts in `domain/repositories/`
3. Create use cases in `domain/usecases/`
4. Implement models and data sources in `data/`
5. Build UI in `presentation/`
6. Configure DI in `core/di/injection.dart`
7. Run: `flutter run`
