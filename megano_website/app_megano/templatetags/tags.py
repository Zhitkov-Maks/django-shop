from django import template

from app_megano.models import Category

register = template.Library()


@register.simple_tag()
def all_categories():
    return Category.objects.filter(active=True).order_by('name')
