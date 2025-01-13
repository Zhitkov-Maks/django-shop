from typing import List, Dict

from django.db.models import QuerySet, Count
from django.views.generic import ListView

from app_megano.crud import add_product_filter, search_product_queryset, add_queryset_top
from app_megano.models import Goods
from app_megano.services import add_data_filter



class SearchProduct(ListView):
    """Класс для поиска товаров по вводу пользователя"""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем queryset для поиска, сортируем по дате создания
        товара, поиск по названию товара.
        """
        return search_product_queryset(self.request.GET.get("query").split())

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update({"query": self.request.GET.get("query")})
        return context


class SearchFilter(ListView):
    """Класс для поиска товаров по вводу пользователя"""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределяем queryset для поиска"""
        return add_product_filter(self.request)

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        add_data_filter(self.request, context)
        return context


class CatalogSortView(ListView):
    """Класс для сортировки товаров по цене (дешевые/дорогие)."""

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: str = 8

    def get_queryset(self) -> QuerySet:
        """
        Переопределяем метод, чтобы получать вариант сортировки,
        и на основе этого и сортировать товары.
        """

        queryset: QuerySet = Goods.objects.prefetch_related("tag").all()

        # Определяем текущий порядок сортировки
        sort_order: str = self.request.GET.get('sort', 'popular')
        direction: str = self.request.GET.get('direction', 'asc')

        if sort_order == 'price':
            queryset = queryset.order_by('price' if direction == 'asc' else '-price')

        elif sort_order == 'reviews':
            queryset = (queryset.annotate(
                count=Count("goods"))
                        .order_by('count' if direction == 'asc' else '-count')
                        )
        elif sort_order == 'newest':
            queryset = queryset.order_by('date_create' if direction == 'asc' else '-date_create')

        elif sort_order == 'popular':
            queryset = add_queryset_top()

        return queryset

    def get_context_data(self, **kwargs) -> List[Dict[str, str]]:
        context = super().get_context_data(**kwargs)

        # Определяем текущий порядок сортировки
        current_sort_key: str = self.request.GET.get('sort', 'popular')
        current_direction: str = self.request.GET.get('direction', 'asc')

        # Определяем доступные параметры сортировки
        context['sort_options']: List[Dict[str, str]] = [
            {'key': 'popular', 'label': 'Популярности', 'direction': current_direction},
            {'key': 'price', 'label': 'Цене', 'direction': current_direction},
            {'key': 'reviews', 'label': 'Отзывам', 'direction': current_direction},
            {'key': 'newest', 'label': 'Новизне', 'direction': current_direction},
        ]

        # Обновляем направление для сортировок
        for option in context['sort_options']:
            if option['key'] == current_sort_key:
                option['direction'] = 'desc' if current_direction == 'asc' else 'asc'

        context['current_sort_key'] = current_sort_key
        return context
