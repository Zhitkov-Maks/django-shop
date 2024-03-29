from django.conf import settings
from django.db import models

from app_megano.models import Goods


class Status(models.Model):
    status = models.CharField(verbose_name='Статус', max_length=50)

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'


class Order(models.Model):
    TYPE_DELIVERY = (
        ('express', 'Экспресс доставка'),
        ('simple', 'Обычная доставка'),
    )

    TYPE_PAYMENT = (
        ('cart', 'Онлайн картой'),
        ('random', 'Онлайн со случайного чужого счета'),
    )

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users',
                             verbose_name='Пользователь')
    type_payment = models.CharField(verbose_name='Тип платежа', choices=TYPE_PAYMENT, max_length=10, default='cart')
    type_delivery = models.CharField(verbose_name='Тип доставки', choices=TYPE_DELIVERY, max_length=10, default='simple')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(verbose_name='Общая стоимость', decimal_places=2, max_digits=8, default=0)
    status = models.ForeignKey(Status, verbose_name='Статус', related_name='statuses', on_delete=models.CASCADE)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    comment = models.TextField(max_length=100, verbose_name='Комментарий', null=True)

    def __str__(self):
        return f'{self.user} / {self.city} / {self.address}'

    class Meta:
        ordering = ('-order_date',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def get_type_payment(self):
        """Для полноценного отображения выбранного типа платежа в шаблоне"""
        if self.type_payment == 'cart':
            return str(Order.TYPE_PAYMENT[0][1])
        elif self.type_payment == 'random':
            return str(Order.TYPE_PAYMENT[1][1])

    def get_type_delivery(self):
        """Для полноценного отображения выбранной доставки в шаблоне"""
        if self.type_delivery == 'express':
            return str(Order.TYPE_DELIVERY[0][1])
        elif self.type_delivery == 'simple':
            return str(Order.TYPE_DELIVERY[1][1])

    @classmethod
    def get_payment(cls, type_payment):
        """Для полноценной записи типа платежа в заказ"""
        if type_payment == 'cart':
            return str(Order.TYPE_PAYMENT[0][1])
        elif type_payment == 'random':
            return str(Order.TYPE_PAYMENT[1][1])

    @classmethod
    def get_delivery(cls, type_delivery):
        """Для полноценной записи платежа в заказ"""
        if type_delivery == 'express':
            return str(Order.TYPE_DELIVERY[0][1])
        elif type_delivery == 'simple':
            return str(Order.TYPE_DELIVERY[1][1])


class DetailOrder(models.Model):
    """Модель для добавления подробной информации о заказе"""
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Goods, verbose_name='goods', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=8)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        verbose_name = 'единица заказа'
        verbose_name_plural = 'детали заказа'
