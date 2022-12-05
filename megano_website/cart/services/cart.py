from django.conf import settings


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        pass

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        pass

    def save(self):
        # Обновление сессии cart
        pass

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        pass

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        pass

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        pass

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        pass

    def clear(self):
        # удаление корзины из сессии
        pass
