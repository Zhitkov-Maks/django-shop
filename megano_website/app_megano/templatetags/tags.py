from django import template

# from app_megano.models import Categories

register = template.Library()


@register.simple_tag()
def all_categories():
    """Для теста создал пока что просто кортеж."""
    list_categories = ('Смартфоны', 'Ноутбуки', 'Аксессуары', 'Наушники', 'Видеокарты', 'Процессоры', 'Мониторы')
    return sorted(list_categories)
