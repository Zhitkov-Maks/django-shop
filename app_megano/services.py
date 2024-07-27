"""Модуль для операций с бд, чтобы не делать это во view, а также при
необходимости использовать в другом месте."""

from _decimal import Decimal
from datetime import timedelta
from typing import List, Dict, Tuple
from datetime import datetime

from django.db.models import Min, Count, Q, QuerySet
from django.utils import timezone

from .models import Category, ViewedProduct, Goods, Discount


def add_category_favorite() -> Dict[int, tuple]:
    """
    Функция для получения 3 избранных категорий(для отображения на главной
    странице в самом верху). Так же к категории добавляем сразу минимальную
    цену в этой категории.
    """
    category_favorite_list: list = Category.objects.filter(favorite=True)[:3]
    category_favorite_dict: Dict[int, tuple] = {}

    for category in category_favorite_list:
        category_favorite_dict[category.id] = (
            category,
            category.categories.aggregate(Min("price")),
        )
    return category_favorite_dict


def add_queryset_top() -> QuerySet:
    """
    Функция для получения списка самых продаваемых товаров за
    последние два месяца.
    """
    end_datetime: datetime = timezone.now()
    start_datetime: datetime = end_datetime - timedelta(days=60)
    queryset = (
        Goods.objects.prefetch_related("tag")
        .annotate(count=Count("shipments"))
        .filter(
            Q(
                shipments__date_purchases__gte=start_datetime,
                shipments__date_purchases__lte=end_datetime,
            )
        )
        .order_by("-count")
    )
    return queryset


def get_viewed_product_period(product) -> int:
    """Получаем количество просмотров товара за полгода."""
    end_datetime: datetime = timezone.now()
    start_datetime: datetime = end_datetime - timedelta(days=180)

    count_viewed: int = (
        ViewedProduct.objects.filter(goods_id=product.id)
        .filter(
            viewed_date__gte=start_datetime, viewed_date__lte=end_datetime
        )
        .count()
    )
    return count_viewed


def check_product_in_cart(cart, product) -> tuple:
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


def add_product_in_viewed_list(user, product) -> None:
    """
    Функция для добавления к пользователю просмотренного товара.
    Если товар ранее уже был просмотрен, то обновляем дату просмотра.
    """
    if ViewedProduct.objects.filter(
            user_id=user.id, goods_id=product.id
    ).exists():
        viewed_product: ViewedProduct = ViewedProduct.objects.get(
            user_id=user.id, goods_id=product.id
        )
        viewed_product.viewed_date = timezone.now()
        viewed_product.save()

    else:
        ViewedProduct.objects.create(
            user=user, goods=product, viewed_date=timezone.now()
        )


def add_product_filter(request) -> QuerySet:
    """Функция для поиска товара по выбранным параметрам."""
    price: list = request.GET.get("price").split(";")
    price_range: tuple = (Decimal(price[0]), Decimal(price[1]))

    name: list = request.GET.get("title").split()
    active: str = request.GET.get("active")
    delivery: str = request.GET.get("delivery")

    query_name, query_descr, query_info = Q(), Q(), Q()
    for word in name:
        query_name &= Q(name__iregex=word)
        query_descr &= Q(description__iregex=word)
        query_info &= Q(detail__info__iregex=word)

    queryset = (
        Goods.objects.prefetch_related("tag")
        .filter(
            Q(query_name, price__range=price_range)
            | Q(query_info, price__range=price_range)
            | Q(query_descr, price__range=price_range)
        )
        .distinct()
    )

    if active == "on":
        queryset = list(filter(lambda x: x.is_active, queryset))
    if delivery == "on":
        queryset = list(filter(lambda x: x.free_delivery, queryset))
    return queryset


def add_data_filter(request, context) -> dict:
    """Функция для получения данных которые ввел пользователь, чтобы после перезагрузки были
    выставлены параметры введенные пользователем."""
    price = request.GET.get("price").split(";")
    title = request.GET.get("title")
    active, delivery = "", ""
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


def clean_no_active_discount() -> None:
    """Функция для перевода закончившихся акций в статус неактивна"""
    current_date = timezone.now()
    product_discount_ended = Discount.objects.filter(valid_to__lt=current_date).filter(
        active=True
    )
    for product in product_discount_ended:
        if product.active:
            product.active = False
            product.save()


def add_product_in_discount() -> None:
    """Проверяем не появилось ли новые активные акции"""
    current_date = timezone.now()
    product_discount_started = Discount.objects.filter(
        valid_from__lte=current_date
    ).filter(valid_to__gte=current_date)
    for product in product_discount_started:
        if not product.active:
            product.active = True
            product.save()


def get_sale():
    """Получаем список акционных товаров, предварительно проверяем на неактивные акции и не появились ли новые"""
    current_date = timezone.now()
    clean_no_active_discount()
    add_product_in_discount()
    queryset = Goods.objects.select_related("discount").filter(
        Q(discount__valid_to__gte=current_date)
    )
    return queryset
