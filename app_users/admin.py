from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CustomUser, Profile


@admin.register(CustomUser)
class UserRegister(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'first_name', 'last_name')
    list_display_links = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'image_show')
    list_display_links = ('user',)

    def image_show(self, rec):
        """Для отображения картинок товаров в админ панели"""
        if rec.photo:
            return mark_safe("<img src='{}' width='60' />".format(rec.photo.url))
        return None

    image_show.__name__ = "Фото"
