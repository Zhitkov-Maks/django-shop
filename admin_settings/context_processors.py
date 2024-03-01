from .models import SiteSettings


def load_settings(request):
    """Функция для получения настроек из базы и передачи их в шаблон"""
    return {'site_settings': SiteSettings.load()}
