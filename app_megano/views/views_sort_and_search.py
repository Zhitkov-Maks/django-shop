from django.db.models import QuerySet, Count
from django.views.generic import ListView

from app_megano.crud import add_product_filter, search_product_queryset
from app_megano.models import Goods
from app_megano.services import add_data_filter


class CatalogSortPrice(ListView):
    """Класс для сортировки товаров начиная с самых дешевых."""

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних обращений к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by("price")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update(
            {"sortPriceMin": True, "header": "Сначала дешевые товары"}
        )
        return context


class CatalogSortPriceMax(ListView):
    """Класс для сортировки товаров начиная с самых дорогих."""

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних обращений к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by("-price")

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context = super().get_context_data()
        context.update(
            {"sortPriceMax": True, "header": "Сначала дорогие товары"}
        )
        return context


class CatalogSortReview(ListView):
    """
    Класс для сортировки товаров по количеству отзывов.
    Сначала выводятся товары где больше всего отзывов.
    """

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределили метод для сортировки."""
        return (
            Goods.objects.prefetch_related("tag")
            .all()
            .annotate(count=Count("goods"))
            .order_by("-count")
        )

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update(
            {
                "sortReview": True,
                "header": "Товары с наибольшим количеством отзывов"
            }
        )
        return context


class CatalogSortReviewMin(ListView):
    """
    Класс для сортировки товаров по количеству отзывов. Сначала выводятся
    товары где меньше всего отзывов.
    """

    model = Goods
    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределили, чтобы добавить сортировку и избежать
        лишних обращений к бд.
        """
        return (
            Goods.objects.prefetch_related("tag")
            .all()
            .annotate(count=Count("goods"))
            .order_by("count")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context = super().get_context_data()
        context.update(
            {
                "sortReviewMin": True,
                "header": "Товары с наименьшим количеством отзывов"
            }
        )
        return context


class CatalogSortNew(ListView):
    """
    Класс для вывода каталога товаров отсортированных по новизне.
    Сначала отображаются товары, которые были добавлены последними.
    """

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: int = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних запросов к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by(
            "-date_create"
        )

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        context.update(
            {"sortNew": True, "header": "Сначала новые товары"}
        )
        return context


class CatalogSortOld(ListView):
    """Сначала отображаются товары, которые были добавлены первыми."""

    template_name: str = "app_megano/catalog.html"
    context_object_name: str = "product_list"
    paginate_by: str = 8

    def get_queryset(self) -> QuerySet:
        """Переопределил, чтобы избежать лишних запросов к бд."""
        return Goods.objects.prefetch_related("tag").all().order_by(
            "date_create"
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет идентификатор для отображения сортировки в шаблоне"""
        context = super().get_context_data()
        context.update(
            {"sortOld": True, "header": "Сначала старые товары"}
        )
        return context


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
        context.update(
            {
                "sortNew": True,
                "header": f"Товары по тэгу {self.request.GET.get('query')}",
                "query": self.request.GET.get("query")}
        )
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
        context.update(
            {
                "sortNew": True,
                "header": "Поиск по параметрам",
                "sortFilter": True
            }
        )
        return context
