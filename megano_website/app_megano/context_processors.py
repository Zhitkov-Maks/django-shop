from django.db.models import Min, Max

from .models import Tags, Goods


def load_tag(request):
    """Функция для вывода тегов в catalog.html. Сделал так как уже минимум в трех местах был повторяющийся код."""
    return {'tag_list': Tags.objects.all()}


def price_min(request):
    return Goods.objects.aggregate(Min('price'))


def price_max(request):
    return Goods.objects.aggregate(Max('price'))
