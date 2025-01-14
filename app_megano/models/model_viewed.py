from django.conf import settings
from django.db import models
from django.db.models import ForeignKey, IntegerField, DateTimeField

from .model_goods import Goods


class ViewedProduct(models.Model):
    """Модель для хранения просмотренных товаров"""

    goods: ForeignKey = models.ForeignKey(
        Goods,
        verbose_name="Товар",
        on_delete=models.CASCADE,
        related_name="products"
    )
    user: ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="persons",
    )
    quantity: IntegerField = models.IntegerField(default=1)
    viewed_date: DateTimeField = models.DateTimeField()

    def __str__(self):
        """Возвращаем строку из названия товара."""
        return f"{self.goods}"
