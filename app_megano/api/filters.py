from django_filters import rest_framework as filters

from ..models import Goods


class GoodsFilter(filters.FilterSet):
    price = filters.BaseRangeFilter(field_name='price')
    date_create_max = filters.IsoDateTimeFilter(field_name='date_create', lookup_expr='lte')
    date_create_min = filters.IsoDateTimeFilter(field_name='date_create', lookup_expr='gte')
    fields = ['is_active', 'free_delivery', 'tag', 'category']

    class Meta:
        model = Goods
        fields = ['is_active', 'free_delivery', 'tag', 'category']
