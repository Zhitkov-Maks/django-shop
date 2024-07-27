from typing import List

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import (
    CharField,
    FileField,
    BooleanField,
    SlugField,
    ManyToManyField,
    ImageField,
    TextField,
    DecimalField,
    PositiveIntegerField,
    DateTimeField, OneToOneField, IntegerField, ForeignKey, EmailField
)
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


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


class Detail(models.Model):
    """Модель для хранения информации о товаре"""

    type: CharField = models.CharField(
        max_length=40, verbose_name="Название атрибута"
    )
    info: CharField = models.CharField(
        max_length=200, verbose_name="Значение"
    )

    def __str__(self):
        """Возвращаем строку из названия атрибута и его значения."""
        return f"{self.type} - {self.info}"

    class Meta:
        verbose_name: str = "детали"
        verbose_name_plural: str = "детали"
        unique_together: tuple = (
            "type",
            "info",
        )


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
    name: CharField = models.CharField(max_length=200, verbose_name="Название")
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
        ordering: tuple = ("valid_from",)
        verbose_name: str = "скидка"
        verbose_name_plural: str = "скидки"


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
