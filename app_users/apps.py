from django.apps import AppConfig


class AppUserConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "app_users"
