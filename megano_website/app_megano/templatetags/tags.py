from django import template
from django.db.models import Count, Min, Max

from app_megano.models import Category, Tags, Goods

register = template.Library()


@register.simple_tag(name='get_cats')
def all_categories():
    """Функция возвращает список категорий"""
    return Category.objects.filter(active=True).order_by('name')


@register.simple_tag(name='get_tags')
def load_tag() -> dict:
    """Функция для вывода тегов в catalog.html. Сделал так как уже минимум в трех местах был повторяющийся код."""
    tags = Tags.objects.annotate(Count('tags')).order_by('-tags__count')[:10]
    return tags


@register.simple_tag(name='get_priceMin')
def price_min() -> dict:
    """Функция для возврата минимальной цены для страницы с каталогом товаров"""
    return Goods.objects.aggregate(Min('price'))


@register.simple_tag(name='get_priceMax')
def price_max() -> dict:
    """Функция для возврата максимальной цены для страницы с каталогом товаров"""
    return Goods.objects.aggregate(Max('price'))
