from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OneToOneField, ImageField
from django.db.models.fields import EmailField, CharField

from .usermanager import CustomUserManager


class CustomUser(AbstractUser):
    """
    Наследуемся от AbstractUser для того, чтобы регистрировать
    пользователя по email.
    """

    username: None = None
    email: EmailField = models.EmailField(
        "email address", unique=True
    )

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Расширяем стандартную таблицу пользователя для добавления
    телефона и аватарки.
    """

    user: OneToOneField = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    patronymic: CharField = models.CharField(
        max_length=20, verbose_name="Отчество"
    )
    photo: ImageField = models.ImageField(
        upload_to="files/image", verbose_name="Фото", blank=True
    )
    phone: CharField = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
