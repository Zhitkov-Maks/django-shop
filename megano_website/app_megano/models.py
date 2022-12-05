# from django.db import models
#
#
# class Tags(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Тэги')
#
#     def __str__(self):
#         return str(self.name)
#
#     class Meta:
#         verbose_name = 'тэг'
#         verbose_name_plural = 'тэги'
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=20, verbose_name='Категория')
#     icon = models.FileField(upload_to='files', blank=True, verbose_name='Иконка')
#     favorite = models.BooleanField(verbose_name='Избранная', default=False)
#     image = models.FileField(upload_to='files', null=True, blank=True, verbose_name='Картинка')
#
#     def __str__(self):
#         return str(self.name)
#
#     class Meta:
#         verbose_name = 'категория'
#         verbose_name_plural = 'категории'
#
#
# class Detail(models.Model):
#     type = models.CharField(max_length=40, verbose_name='Тип')
#     info = models.CharField(max_length=200, verbose_name='Описание')
#
#     def __str__(self):
#         return f'{self.type} - {self.info}'
#
#     class Meta:
#         verbose_name = 'детали'
#         verbose_name_plural = 'детали'
#
#
# class Goods(models.Model):
#     category = models.ForeignKey(Category, verbose_name='Категория', related_name='categories',
#                                  on_delete=models.CASCADE)
#     tag = models.ManyToManyField(Tags, verbose_name='тэг', related_name='tags')
#     detail = models.ManyToManyField(Detail, verbose_name='детали', related_name='details')
#     image = models.ImageField(upload_to='files/images/', verbose_name='Основная фотография')
#     name = models.CharField(max_length=200, verbose_name='Название')
#     description = models.TextField(max_length=2000, verbose_name='Описание')
#     price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2)
#     stock = models.PositiveIntegerField(verbose_name='Остаток')
#     limited_edition = models.BooleanField(default=False, verbose_name='Ограниченная серия')
#     date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#
#     def __str__(self):
#         return str(self.name)
#
#     class Meta:
#         verbose_name = 'товар'
#         verbose_name_plural = 'товары'
#
#
# class Gallery(models.Model):
#     """Для добавления еще нескольких фотографий для товара"""
#     image = models.ImageField(upload_to='gallery')
#     goods = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='images', verbose_name='Фото')
#
#     class Meta:
#         verbose_name = 'еще фотография'
#         verbose_name_plural = 'добавить фотографий'
#
#
# class Comment(models.Model):
#     goods = models.ForeignKey(Goods, verbose_name='Товар', related_name='goods', on_delete=models.CASCADE)
#     name = models.CharField(max_length=30, verbose_name='Имя')
#     email = models.EmailField(verbose_name='Email')
#     comment = models.TextField(max_length=2000, verbose_name='Комментарий')
#     active = models.BooleanField(verbose_name='Активен')
#
#     def __str__(self):
#         return f'{self.goods} / {self.name} / {str(self.comment)[:15]}'
#
#     class Meta:
#         verbose_name = 'комментарий'
#         verbose_name_plural = 'комментарии'
#
#
# class Purchases(models.Model):
#     goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар', related_name='product')
#     count = models.PositiveIntegerField(verbose_name='Количество')
#     date_purchases = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.goods)
#
#     class Meta:
#         verbose_name = 'покупка'
#         verbose_name_plural = 'покупки'
