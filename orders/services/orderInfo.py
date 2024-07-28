from typing import Tuple
from unicodedata import decimal

from django.conf import settings
from django.http import HttpRequest

from admin_settings.models import SiteSettings
from cart.services.cart import Cart
from orders.forms import OrderForms
from orders.models import Order


class OrderInfo(object):
    """
    Класс для хранения информации о заказе в сессии. Нужен для при
    оформлении заказа, чтобы вывести введенные пользователем данные.
    """

    def __init__(self, request: HttpRequest):
        """Инициализируем заказ."""
        self.session = request.session
        order: dict = self.session.get(settings.ORDER_SESSION_INFO)

        if not order:
            order = self.session[settings.ORDER_SESSION_INFO] = {}
        self.order = order

    def add(self, form: OrderForms, request: HttpRequest) -> None:
        """Добавить заказ в словарь из сессии."""
        type_delivery: str = Order.get_delivery(
            form.cleaned_data.get("type_delivery")
        )
        type_payment: str = Order.get_payment(
            form.cleaned_data.get("type_payment")
        )
        delivery_price, total_price = get_delivery_price(
            form.cleaned_data.get("type_delivery"), request
        )

        self.order["order"] = {
            "full_name": form.cleaned_data.get("full_name"),
            "city": form.cleaned_data.get("city"),
            "email": form.cleaned_data.get("email"),
            "phone": form.cleaned_data.get("phone"),
            "address": form.cleaned_data.get("address"),
            "type_delivery": type_delivery,
            "type_payment": type_payment,
            "delivery_price": delivery_price,
            "total_price": total_price,
        }
        self.save()

    def save(self):
        self.session[settings.ORDER_SESSION_INFO] = self.order
        self.session.modified = True

    def get_total_price(self) -> int:
        """Получаем общую сумму заказа."""
        return self.order["order"]["total_price"]

    def __iter__(self):
        """Перебор элементов в заказе и получение информации из сессии."""
        order: dict = self.order
        for item in order:
            item = order[item]
            yield item


def get_delivery_price(
        type_delivery: str,
        request: HttpRequest
) -> Tuple[float, float]:
    """
    Функция для получения стоимости доставки, в зависимости от суммы
    и выбранной доставки.
    """
    price: int = 0

    # Получаем стоимость доставки
    admin_settings: SiteSettings = SiteSettings.objects.all()[0]
    cart: Cart = Cart(request)

    if type_delivery == "express":
        price = admin_settings.price_delivery_express

    elif type_delivery == "simple":
        price = admin_settings.price
        min_sum: int = admin_settings.min_sum

        if cart.get_total_price() >= min_sum:
            price = decimal("0")

    total_price: int = cart.get_total_price() + price
    return float(price), float(total_price)
