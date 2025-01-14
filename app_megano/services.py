"""Модуль для операций, чтобы не делать это во view, а также при
необходимости использовать в другом месте."""
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from app_users.models import CustomUser
from cart.services.cart import Cart
from .crud import get_viewed_product_period, add_product_in_viewed_list
from .models import Goods, Comment


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


def add_data_filter(request: WSGIRequest, context: dict) -> dict:
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


def collection_data(product_detail_view, context: dict) -> None:
    # Проверяем есть ли данный товар в корзине.
    check: tuple = check_product_in_cart(
        Cart(product_detail_view.request),
        product_detail_view.object
    )

    # Получаем количество просмотров за неделю
    count_viewed: int = get_viewed_product_period(product_detail_view.object)

    user: CustomUser = product_detail_view.request.user

    # Добавляем товар в просмотренные
    if product_detail_view.request.user.is_authenticated:
        add_product_in_viewed_list(user, product_detail_view.get_object())

    product: Goods = product_detail_view.get_object()
    comment: QuerySet = (
        Comment.objects
        .select_related('user', 'user__profile')
        .filter(goods_id=product.id)
    )

    detail = product.detail.prefetch_related("details").all()
    context.update(
        {
            "product": product,
            'check': check[0],
            'quantity': check[1],
            'count_viewed': count_viewed,
            'messages': comment,
            'len': len(comment),
            'header': product_detail_view.object,
            'detail': detail
        }
    )
