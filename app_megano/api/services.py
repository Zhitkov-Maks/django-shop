from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination

from .filters import GoodsFilter
from ..models import Goods
from .serializers import ProductSerializers


class PaginationView(PageNumberPagination):
    """Класс для добавления пагинации."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductApi(ListModelMixin, GenericAPIView):
    queryset = Goods.objects.prefetch_related('tag').all()
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    pagination_class = PaginationView
    filterset_class = GoodsFilter
    search_fields = ('$name', '$description')

    def get(self, request):
        """Представление для получения списка книг."""
        return self.list(request)

    def get_queryset(self):
        return Goods.objects.all().order_by('-date_create')
