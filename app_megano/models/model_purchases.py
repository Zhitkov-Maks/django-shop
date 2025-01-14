from django.db import models
from django.db.models import (
    ForeignKey,
    PositiveIntegerField,
    DateTimeField
)

from .model_goods import Goods


class Purchases(models.Model):
    """Модель для хранения истории продаж"""

    goods: ForeignKey = models.ForeignKey(
        Goods,
        verbose_name="Товар",
        on_delete=models.CASCADE,
        related_name="shipments"
    )
    quantity: PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="Количество"
    )
    date_purchases: DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Возвращаем строку из товара, количества и даты продажи."""
        return f"{self.goods} {self.quantity} {self.date_purchases}"
