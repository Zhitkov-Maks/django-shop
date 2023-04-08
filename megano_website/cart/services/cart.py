import copy
from decimal import Decimal

from django.conf import settings

from app_megano.models import Goods


class Cart(object):

    def __init__(self, request):
        """Инициализируем корзину"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавить продукт в корзину или обновить его количество."""
        product_id = str(product.id)
        if product_id not in self.cart:
            price_discount = 0.0
            if hasattr(product, 'discount'):
                if product.discount.active:
                    coefficient = round(product.discount.discount / 100, 2)
                    price_discount = round(float(product.price) * coefficient, 2)
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(round(float(product.price) - price_discount, 2)),
                                     'discount': str(price_discount)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Обновление сессии cart"""
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Goods.objects.filter(id__in=product_ids)
        cart = copy.deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = round(float(item['price']), 2)
            item['total_price'] = round(item['price'] * item['quantity'], 2)
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине."""
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def get_total_discount(self):
        """Подсчет общей скидки в корзине."""
        total_discount = sum(Decimal(dis['discount']) * dis['quantity'] for dis in self.cart.values())
        return total_discount

    def clear(self):
        """Удаление корзины из сессии"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
