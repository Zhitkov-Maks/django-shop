from django.contrib import admin
from django.db.utils import ProgrammingError

from .models import SiteSettings


class SiteSettingsAdmin(admin.ModelAdmin):
    # Переопределяем метод get_queryset для выполнения логики загрузки настроек
    def get_queryset(self, request):
        # Получаем стандартный queryset
        qs = super().get_queryset(request)
        try:
            # Пытаемся загрузить настройки при первом запросе
            settings = SiteSettings.load()
            # Если queryset пустой, сохраняем загруженные настройки
            if not qs.exists():
                settings.save()
        except ProgrammingError:
            # Игнорируем ошибку, если таблица не создана
            pass
        return qs

    # Запрещаем добавление новых объектов в админке
    def has_add_permission(self, request, obj=None):
        return False

    # Запрещаем удаление объектов в админке
    def has_delete_permission(self, request, obj=None):
        return False


# Регистрируем модель SiteSettings с кастомным администратором
admin.site.register(SiteSettings, SiteSettingsAdmin)
