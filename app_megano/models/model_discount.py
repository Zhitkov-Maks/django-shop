from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (
    OneToOneField,
    DateTimeField,
    IntegerField,
    BooleanField,
    TextField
)

from .model_goods import Goods


class Discount(models.Model):
    """Модель для представления скидок на товары."""
    product: OneToOneField = models.OneToOneField(
        Goods, verbose_name="Товар", on_delete=models.CASCADE
    )
    valid_from: DateTimeField = models.DateTimeField(
        verbose_name="Начало акции"
    )
    valid_to: DateTimeField = models.DateTimeField(verbose_name="Конец акции")
    discount: IntegerField = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Скидка в %",
    )
    active: BooleanField = models.BooleanField(verbose_name="Активность")
    description: TextField = models.TextField(
        verbose_name="Описание скидки", max_length=200
    )

    def __str__(self):
        """Возвращаем строку с названием продукта."""
        return str(self.product)

    class Meta:
        ordering: tuple = "valid_from",
        verbose_name: str = "скидка"
        verbose_name_plural: str = "скидки"
