from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, DetailProduct, SaleView, CatalogView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/', DetailProduct.as_view(), name='detail'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
