import random
from typing import Tuple

from django.db import transaction
from django.db.models.fields import PositiveIntegerField
from django.http import HttpRequest

from app_users.models import CustomUser
from orders.forms import OrderForms
from orders.models import Status, DetailOrder, Order
from cart.services.cart import Cart
from app_megano.models import Purchases, Goods


def add_order(
        form: OrderForms,
        user: CustomUser,
        total_price: int
) -> Tuple[Order, str]:
    """
    Добавляем информацию о заказе. Возвращаем заказ и тип платежа чтобы в
    зависимости от выбранного платежа перенаправить на нужную страницу.
    """
    order: Order = form.save(commit=False)

    order.total_price = total_price
    order.user_id = user.id
    order.status = Status.objects.get(id=2)

    order.save()
    return order, order.type_payment


@transaction.atomic
def add_detail_to_order(order: Order, request: HttpRequest) -> None:
    """Добавляем к заказу товары из которых он состоит."""
    cart: Cart = Cart(request)
    for item in cart:
        DetailOrder.objects.create(
            order=order,
            product=item["product"],
            price=item["price"],
            quantity=item["quantity"],
        )

        Purchases.objects.create(
            goods=item["product"],
            quantity=item["quantity"]
        )
        product: Goods = Goods.objects.get(id=item["product"].id)
        product.stock -= item["quantity"]

        # Проверяем не закончился ли товар, если закончился то
        # переводим в статус не активен
        if product.stock == 0:
            product.is_active = False
        product.save()

    # Очищаем корзину
    cart.clear()


def check_cart(cart: Cart) -> bool:
    """Проверяем не закончился ли товар, который есть в корзине."""
    stock: bool = True
    for item in cart:
        product: Goods = Goods.objects.get(id=item["product"].id)
        if not product.is_active:
            stock = False
    return stock


def get_number_card(form: OrderForms, order: Order):
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
        "".join([
            item for item in form.cleaned_data.get("number") if item.isdigit()
        ])
    )

    if card_number % 10 == 0 or card_number % 10 == 6:
        order.comment = random.choice(list_payment_failed)

    else:
        order.status = Status.objects.get(pk=1)
        order.paid = True
        order.comment = None
    order.save()
