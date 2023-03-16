from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Tags(models.Model):
    """Модель для добавления тегов"""
    name = models.CharField(max_length=20, verbose_name='Теги')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Category(MPTTModel):
    """Модель для представления категорий."""
    name = models.CharField(max_length=20, verbose_name='Категория')
    icon = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Иконка')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    favorite = models.BooleanField(verbose_name='Избранная', default=False)
    active = models.BooleanField(verbose_name='Активность', default=False)
    image = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Картинка')
    slug = models.SlugField()

    def __str__(self):
        return str(self.name)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def get_absolute_url(self):
        return reverse('post-by-category', args=[str(self.slug)])


class Detail(models.Model):
    """Модель для хранения информации о товаре"""
    type = models.CharField(max_length=40, verbose_name='Тип')
    info = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return f'{self.type} - {self.info}'

    class Meta:
        verbose_name = 'детали'
        verbose_name_plural = 'детали'
        unique_together = ('type', 'info',)


class Goods(models.Model):
    """Модель для представления товаров."""
    category = models.ManyToManyField(Category, verbose_name='Категория', related_name='categories')
    tag = models.ManyToManyField(Tags, verbose_name='тэг', related_name='tags')
    detail = models.ManyToManyField(Detail, verbose_name='детали', related_name='details')
    image = models.ImageField(upload_to='files/images/', verbose_name='Основная фотография')
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    limited_edition = models.BooleanField(default=False, verbose_name='Ограниченная серия')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    free_delivery = models.BooleanField(verbose_name='Бесплатная доставка', default=False)

    def __str__(self):
        return f'{str(self.name)[:40]}...'

    class Meta:
        ordering = ('-date_create',)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Discount(models.Model):
    product = models.OneToOneField(Goods, verbose_name='Товар', on_delete=models.CASCADE)
    valid_from = models.DateTimeField(verbose_name='Начало акции')
    valid_to = models.DateTimeField(verbose_name='Конец акции')
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Скидка в %')
    active = models.BooleanField(verbose_name='Активность')
    description = models.TextField(verbose_name='Описание скидки', max_length=200)

    def __str__(self):
        return str(self.product)

    class Meta:
        ordering = ('valid_from',)
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Gallery(models.Model):
    """Для добавления еще нескольких фотографий для товара"""
    image = models.ImageField(upload_to='gallery')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images', verbose_name='Фото')

    class Meta:
        verbose_name = 'еще фотография'
        verbose_name_plural = 'добавить фотографий'


class Comment(models.Model):
    """Модель для добавления комментариев"""
    goods = models.ForeignKey(Goods, verbose_name='Товар', related_name='goods', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='comments', default=None, null=True)
    name = models.CharField(max_length=30, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(max_length=2000, verbose_name='Комментарий')
    active = models.BooleanField(verbose_name='Активен', default=True)
    date_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.goods} / {self.name} / {str(self.comment)[:15]}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('date_comment',)


class ViewedProduct(models.Model):
    """Модель для хранения просмотренных товаров"""
    goods = models.ForeignKey(Goods, verbose_name='Товар', on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='persons')
    quantity = models.IntegerField(default=1)
    viewed_date = models.DateTimeField()

    def __str__(self):
        return f'{self.goods} {self.user} {self.viewed_date}'


class Purchases(models.Model):
    """Модель для хранения истории продаж"""
    goods = models.ForeignKey(Goods, verbose_name='Товар', on_delete=models.CASCADE, related_name='shipments')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    date_purchases = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.goods} {self.quantity} {self.date_purchases}'
