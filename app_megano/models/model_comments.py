from django.db import models
from django.db.models import (
    ForeignKey,
    CharField,
    EmailField,
    TextField,
    BooleanField,
    DateTimeField
)

from .model_goods import Goods
from megano_website import settings


class Comment(models.Model):
    """Модель для добавления комментариев"""

    goods: ForeignKey = models.ForeignKey(
        Goods,
        verbose_name="Товар",
        related_name="goods",
        on_delete=models.CASCADE
    )
    user: ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    name: CharField = models.CharField(max_length=30, verbose_name="Имя")
    email: EmailField = models.EmailField(verbose_name="Email")
    comment: TextField = models.TextField(
        max_length=2000, verbose_name="Комментарий"
    )
    active: BooleanField = models.BooleanField(
        verbose_name="Активен", default=False
    )
    date_comment: DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращаем строку из товара, имени и комментария."""
        return f"{self.goods} / {self.name} / {str(self.comment)[:15]}"

    class Meta:
        verbose_name: str = "комментарий"
        verbose_name_plural: str = "комментарии"
        ordering: tuple = ("date_comment",)
