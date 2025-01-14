from django.db import models
from django.db.models import (
    ManyToManyField,
    ImageField,
    TextField,
    DecimalField,
    PositiveIntegerField,
    BooleanField,
    DateTimeField,
    CharField, ForeignKey
)

from .model_tags_categories import Category, Tags


class Detail(models.Model):
    """Модель для хранения информации о товаре"""

    type: CharField = models.CharField(
        max_length=40, verbose_name="Название атрибута", db_index=True
    )
    info: CharField = models.CharField(
        max_length=200, verbose_name="Значение", db_index=True
    )

    def __str__(self):
        """Возвращаем строку из названия атрибута и его значения."""
        return f"{self.type} - {self.info}"

    class Meta:
        verbose_name: str = "детали"
        verbose_name_plural: str = "детали"
        unique_together: tuple = ("type", "info",)


class Goods(models.Model):
    """Модель для представления товаров."""

    category: ManyToManyField = models.ManyToManyField(
        Category, verbose_name="Категория", related_name="categories"
    )
    tag: Tags = models.ManyToManyField(
        Tags, verbose_name="тэг", related_name="tags"
    )
    detail: ManyToManyField = models.ManyToManyField(
        Detail, verbose_name="детали", related_name="details"
    )
    image: ImageField = models.ImageField(
        upload_to="files/images/", verbose_name="Основная фотография"
    )
    name: CharField = models.CharField(
        max_length=200, verbose_name="Название", db_index=True
    )
    description: TextField = models.TextField(
        max_length=2000, verbose_name="Описание"
    )
    price: DecimalField = models.DecimalField(
        verbose_name="Цена", max_digits=8, decimal_places=2
    )
    stock: PositiveIntegerField = models.PositiveIntegerField(
        verbose_name="Остаток"
    )
    limited_edition: BooleanField = models.BooleanField(
        default=False, verbose_name="Ограниченная серия"
    )
    date_create: DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    is_active: BooleanField = models.BooleanField(
        verbose_name="Активен", default=True
    )
    free_delivery: BooleanField = models.BooleanField(
        verbose_name="Бесплатная доставка", default=False
    )

    def __str__(self):
        """Возвращаем строку с именем длиной не более 40 символов."""
        return f"{str(self.name)[:40]}..."

    class Meta:
        ordering: tuple = ("-date_create",)
        verbose_name: str = "товар"
        verbose_name_plural: str = "товары"


class Gallery(models.Model):
    """Для добавления еще нескольких фотографий для товара"""

    image: ImageField = models.ImageField(upload_to="gallery")
    goods: ForeignKey = models.ForeignKey(
        Goods,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Фото"
    )

    class Meta:
        verbose_name: str = "еще фотография"
        verbose_name_plural: str = "добавить фотографий"
