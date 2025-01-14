from typing import List

from django.db import models
from django.db.models import CharField, FileField, BooleanField, SlugField
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Tags(models.Model):
    """Модель для добавления тегов."""

    name: CharField = models.CharField(max_length=20, verbose_name="Теги")

    def __str__(self):
        """Возвращаем название тега."""
        return str(self.name)

    class Meta:
        verbose_name: str = "тег"
        verbose_name_plural: str = "теги"


class Category(MPTTModel):
    """Модель для представления категорий."""

    name: CharField = models.CharField(max_length=20, verbose_name="Категория")
    icon: FileField = models.FileField(
        upload_to="files", null=True, blank=True, verbose_name="Иконка"
    )
    parent: TreeForeignKey = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        verbose_name="Родительская категория",
    )
    favorite: BooleanField = models.BooleanField(
        verbose_name="Избранная", default=False
    )
    active: BooleanField = models.BooleanField(
        verbose_name="Активность", default=False
    )
    image: FileField = models.FileField(
        upload_to="files", null=True, blank=True, verbose_name="Картинка"
    )
    slug: SlugField = models.SlugField()

    def __str__(self):
        """Возвращаем название категории."""
        return str(self.name)

    class MPTTMeta:
        order_insertion_by: List[str] = ["name"]

    class Meta:
        unique_together: List[List[str]] = [["parent", "slug"]]
        verbose_name: str = "категория"
        verbose_name_plural: str = "категории"

    def get_absolute_url(self):
        return reverse("post-by-category", args=[str(self.slug)])
