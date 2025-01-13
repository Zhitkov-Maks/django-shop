from django.http import HttpRequest

from .models import SiteSettings


def load_settings(request: HttpRequest) -> dict:
    """
    Функция для получения настроек из базы и передачи
    их в шаблон дял отображения.
    """
    return {"site_settings": SiteSettings.load()}
