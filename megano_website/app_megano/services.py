from _decimal import Decimal
from datetime import timedelta

from django.db.models import Min, Sum
from django.utils import timezone

from .models import Category, ViewedProduct, Goods, Purchases, Discount


def add_category_favorite() -> dict:
    """Функция для получения 3 избранных категорий(для отображения на главной странице в самом верху)
    Так же к категории добавляем сразу минимальную цену в этой категории"""
    category_favorite_list = Category.objects.filter(favorite=True)[:3]
    category_favorite_dict = {}
    for category in category_favorite_list:
        category_favorite_dict[category.id] = [category, category.categories.aggregate(Min('price'))]
    return category_favorite_dict


def add_queryset_top() -> list:
    """Функция для получения списка самых продаваемых товаров за последние два месяца."""
    end_datetime = timezone.now()
    start_datetime = end_datetime - timedelta(days=60)
    queryset = Purchases.objects.values('goods').distinct().annotate(
        sum=Sum("quantity")
    ).filter(
        date_purchases__gte=start_datetime, date_purchases__lte=end_datetime,
    ).order_by("-sum")
    map_list = map(lambda x: Goods.objects.get(id=x['goods']), queryset)
    product_list = list(filter(lambda product: product.is_active, map_list))
    return product_list


def get_viewed_product_week(product) -> int:
    """Получаем количество просмотров товара за неделю"""
    end_datetime = timezone.now()
    start_datetime = end_datetime - timedelta(days=7)
    count_viewed = ViewedProduct.objects.filter(goods_id=product.id)\
        .filter(viewed_date__gte=start_datetime, viewed_date__lte=end_datetime,)
    return len(count_viewed)


def check_product_in_cart(cart, product):
    """Функция нужна для страницы с описанием товара, чтобы проверить есть ли этот товар в корзине, а если
    есть то узнать количество. Чтобы на странице с товаром уже сразу отображалось что данный товар у пользователя уже в
    корзине."""
    check = False
    quantity = 0
    for detail in cart:
        if detail['product'] == product:
            check = True
            quantity = detail['quantity']
    return check, quantity


def add_product_in_viewed_list(user, product) -> None:
    """Функция для добавления к пользователю просмотренного товара. Если товар ранее уже был просмотрен, то обновляем
    дату просмотра."""
    if ViewedProduct.objects.filter(user_id=user.id, goods_id=product.id).exists():
        viewed_product = ViewedProduct.objects.get(user_id=user.id, goods_id=product.id)
        viewed_product.viewed_date = timezone.now()
        viewed_product.save()
    else:
        ViewedProduct.objects.create(user=user, goods=product, viewed_date=timezone.now())


def add_product_filter(request) -> list:
    """Функция для поиска товара по выбранным параметрам"""
    price = request.GET.get('price').split(';')
    price_range = (Decimal(price[0]), Decimal(price[1]))
    name = request.GET.get('title')
    active = request.GET.get('active')
    delivery = request.GET.get('delivery')

    if active == 'on' and not delivery:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name)\
            .filter(is_active=True).order_by('-date_create')
    elif delivery == 'on' and not active:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name).filter(
            free_delivery=True).order_by('-date_create')
    elif active == 'on' and delivery == 'on':
        queryset = Goods.objects.filter(price__range=price_range). \
            filter(name__iregex=name).filter(is_active=True).filter(free_delivery=True).order_by('-date_create')
    else:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name).order_by('-date_create')
    return queryset


def add_data_filter(request, context):
    """Функция для получения данных которые ввел пользователь, чтобы после перезагрузки были
    выставлены параметры введенные пользователем."""
    price = request.GET.get('price').split(';')
    title = request.GET.get('title')
    active, delivery = '', ''
    if request.GET.get('active') == 'on':
        active = 'on'
    if request.GET.get('delivery') == 'on':
        delivery = 'on'
    context.update({'search': True, 'data_from': price[0], 'data_to': price[1],
                    'active': active, 'delivery': delivery, 'title': title, 'price': f'{price[0]};{price[1]}'})
    return context


def clean_no_active_discount() -> None:
    """Функция для перевода закончившихся акций в статус неактивна"""
    current_date = timezone.now()
    product_discount_ended = Discount.objects.filter(valid_to__lt=current_date).filter(active=True)
    for product in product_discount_ended:
        if product.active:
            product.active = False
            product.save()


def add_product_in_discount() -> None:
    """Проверяем не появилось ли новые активные акции"""
    current_date = timezone.now()
    product_discount_started = Discount.objects.filter(valid_from__lte=current_date).filter(valid_to__gte=current_date)
    for product in product_discount_started:
        if not product.active:
            product.active = True
            product.save()
