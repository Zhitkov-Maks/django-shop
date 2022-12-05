# from django.contrib.auth.models import User
# from django.db import models
#
# from app_megano.models import Goods
#
# class Status(models.Model):
#     status = models.CharField(verbose_name='Статус', max_length=50)
#     comment = models.CharField(verbose_name='Комментарий к статусу', max_length=500, blank=True)
#
#     def __str__(self):
#         return str(self.status)
#
#     class Meta:
#         verbose_name = 'статус'
#         verbose_name_plural = 'статусы'
#
#
# class TypeDelivery(models.Model):
#     type = models.CharField(max_length=50, verbose_name='Тип доставки')
#     initial_cost = models.DecimalField(verbose_name='Начальная стоимость', max_digits=5, decimal_places=2)
#
#     def __str__(self):
#         return str(self.type)
#
#     class Meta:
#         verbose_name = 'доставка'
#         verbose_name_plural = 'типы доставок'
#
#
# class TypePayment(models.Model):
#     type = models.CharField(max_length=50, verbose_name='Тип платежа')
#
#     def __str__(self):
#         return str(self.type)
#
#     class Meta:
#         verbose_name = 'тип платежа'
#         verbose_name_plural = 'типы платежей'
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', verbose_name='Пользователь')
#     type_payment = models.ForeignKey(TypePayment, on_delete=models.CASCADE, verbose_name='Тип платежа')
#     type_delivery = models.ForeignKey(TypeDelivery, on_delete=models.CASCADE, verbose_name='Тип доставки')
#     status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
#     city = models.CharField(max_length=30, verbose_name='Город')
#     address = models.CharField(max_length=100, verbose_name='Адрес')
#     order_date = models.DateTimeField(auto_now_add=True)
#     comment = models.TextField(max_length=300, verbose_name='Комментарий к заказу')
#
#     def __str__(self):
#         return f'{self.user} / {self.city} / {self.address}'
#
#     class Meta:
#         verbose_name = 'заказ'
#         verbose_name_plural = 'заказы'
#
#
# class DetailOrder(models.Model):
#     order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orders', on_delete=models.CASCADE)
#     product = models.OneToOneField(Goods, verbose_name='goods', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#     price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=8)
#
#     def __str__(self):
#         return str(self.product)
#
#     class Meta:
#         verbose_name = 'еденица заказа'
#         verbose_name_plural = 'детали заказа'
