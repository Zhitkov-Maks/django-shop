"""Модуль для операций, чтобы не делать это во view, а также при
необходимости использовать в другом месте."""

from django.http import HttpRequest

from cart.services.cart import Cart
from .models import Goods


def check_product_in_cart(cart: Cart, product: Goods) -> tuple:
    """
    Функция нужна для страницы с описанием товара, чтобы проверить есть ли
    этот товар в корзине, а если есть то узнать количество.
    Чтобы на странице с товаром уже сразу отображалось что данный товар у
    пользователя уже в корзине.
    """
    check: bool = False
    quantity: int = 0
    for detail in cart:
        if detail["product"] == product:
            check = True
            quantity = detail["quantity"]
            break
    return check, quantity


def add_data_filter(request: HttpRequest, context: dict) -> dict:
    """
    Функция для получения данных которые ввел пользователь, чтобы после
    перезагрузки были выставлены параметры введенные пользователем.
    """
    price: list = request.GET.get("price").split(";")
    title: str = request.GET.get("title")
    active: str = ""
    delivery: str = ""

    if request.GET.get("active") == "on":
        active = "on"
    if request.GET.get("delivery") == "on":
        delivery = "on"

    context.update(
        {
            "search": True,
            "data_from": price[0],
            "data_to": price[1],
            "active": active,
            "delivery": delivery,
            "title": title,
            "price": f"{price[0]};{price[1]}",
        }
    )
    return context
