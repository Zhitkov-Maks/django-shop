from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "cart"
