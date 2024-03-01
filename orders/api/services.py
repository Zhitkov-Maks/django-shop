from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializers
from ..models import Order


class PaginationView(PageNumberPagination):
    """Класс для добавления пагинации."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderApi(ListModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    filter_backends = [DjangoFilterBackend]
    pagination_class = PaginationView
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.select_related('status').filter(Q(user_id=self.request.user.id))

    def get(self, request):
        """Представление для получения списка книг."""
        return self.list(request)
