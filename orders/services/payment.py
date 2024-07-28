import random

from django.db import transaction

from orders.models import Status, DetailOrder
from cart.services.cart import Cart
from app_megano.models import Purchases, Goods


def add_order(form, user, total_price) -> tuple:
    """Добавляем информацию о заказе. Возвращаем заказ и тип платежа чтобы в зависимости от выбранного платежа
    перенаправить на нужную страницу"""
    order = form.save(commit=False)
    order.total_price = total_price
    order.user_id = user.id
    order.status = Status.objects.get(pk=2)
    order.save()
    return order, order.type_payment


@transaction.atomic
def add_detail_to_order(order, request) -> None:
    """Добавляем к заказу товары из которых он состоит."""
    cart = Cart(request)
    for item in cart:
        DetailOrder.objects.create(
            order=order,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )
        Purchases.objects.create(goods=item["product"], quantity=item["quantity"])
        product = Goods.objects.get(id=item["product"].id)
        product.stock -= item["quantity"]
        # Проверяем не закончился ли товар, если закончился то переводим в статус не активен
        if product.stock <= 0:
            product.is_active = False
        product.save()
    cart.clear()


def check_cart(cart) -> bool:
    """Проверяем не закончился ли товар, который есть в корзине."""
    stock = True
    for item in cart:
        product = Goods.objects.get(id=item["product"].id)
        if not product.is_active:
            stock = False
    return stock


def get_number_card(form, order):
    """Проверяем номер карты на валидность условиям."""
    list_payment_failed = [
        "Недостаточно средств",
        "Ошибка соединения с платежной системой",
        "Сервер занят попробуйте позже",
        "Подозрение на спам",
        "Слишком часто заказываете у нас",
    ]
    # Проверяем номер карты на соответствие условиям платежа
    card_number = int(
        "".join([item for item in form.cleaned_data.get("number") if item.isdigit()])
    )
    if card_number % 10 == 0 or card_number % 10 == 6:
        order.comment = random.choice(list_payment_failed)
    else:
        order.status = Status.objects.get(pk=1)
        order.paid = True
        order.comment = None
    order.save()
