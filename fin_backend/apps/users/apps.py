from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # The 'name' must be the full Python path!
    name = "apps.users"
    # 'label' keeps your database tables named cleanly (e.g., 'users_user')
    label = "users"
