from _decimal import Decimal
from datetime import timedelta

from django.db.models import Min, Sum
from django.utils import timezone

from .models import Category, ViewedProduct, Goods, Purchases


def add_category_favorite():
    favorite = Category.objects.filter(favorite=True)[:3]
    category_dict = {}
    for cat in favorite:
        category_dict[cat.id] = [cat, cat.categories.aggregate(Min('price'))]
    return category_dict


def add_queryset_top():
    end_datetime = timezone.now()
    start_datetime = end_datetime - timedelta(days=60)
    queryset = Purchases.objects.values('goods').distinct().annotate(
        sum=Sum("quantity")
    ).filter(
        date_purchases__gte=start_datetime, date_purchases__lte=end_datetime
    ).order_by("-sum")
    product_list = list(map(lambda x: Goods.objects.get(id=x['goods']), queryset))
    return product_list


def check_product_in_cart(cart, product):
    check = False
    quantity = 0
    for detail in cart:
        if detail['product'] == product:
            check = True
            quantity = detail['quantity']
    return check, quantity


def add_product_in_top_list(user, product):
    if ViewedProduct.objects.filter(user_id=user.id, goods_id=product.id).exists():
        viewed_product = ViewedProduct.objects.get(user_id=user.id, goods_id=product.id)
        viewed_product.viewed_date = timezone.now()
        viewed_product.save()
    else:
        ViewedProduct.objects.create(user=user, goods=product, viewed_date=timezone.now())


def add_product_filter(request):
    price = request.GET.get('price').split(';')
    name = request.GET.get('title')
    active = request.GET.get('active')
    delivery = request.GET.get('delivery')
    price_range = (Decimal(price[0]), Decimal(price[1]))
    if active == 'on' and not delivery:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name).filter(is_active=True)
    elif delivery == 'on' and not active:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name).filter(
            free_delivery=True)
    elif active == 'on' and delivery == 'on':
        queryset = Goods.objects.filter(price__range=price_range). \
            filter(name__iregex=name).filter(is_active=True).filter(free_delivery=True)
    else:
        queryset = Goods.objects.filter(price__range=price_range).filter(name__iregex=name)
    return queryset


def add_data_filter(request, context):
    price = request.GET.get('price').split(';')
    title = request.GET.get('title')
    active, delivery = False, False
    if request.GET.get('active') == 'on':
        active = True
    if request.GET.get('delivery') == 'on':
        delivery = True
    context.update({'search': True, 'data_from': price[0], 'data_to': price[1],
                    'active': active, 'delivery': delivery, 'title': title})
    return context
