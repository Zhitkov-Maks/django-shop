from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, SaleView, CatalogView, ShowCategory, ProductDetailView, ShowTag, ViewedProducts

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('categories/<int:pk>/', ShowCategory.as_view(), name="category"),
    path('tags/<int:pk>/', ShowTag.as_view(), name="tag"),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('viewed/<int:pk>', ViewedProducts.as_view(), name='viewed')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
