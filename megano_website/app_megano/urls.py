from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, CatalogView, ShowCategory, ProductDetailView, ShowTag, ViewedProducts, \
    CatalogSortPrice, CatalogSortReview, CatalogSortNew, CatalogSortPriceMax, SearchProduct, SearchFilter

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('categories/<int:pk>/', ShowCategory.as_view(), name="category"),
    path('tags/<int:pk>/', ShowTag.as_view(), name="tag"),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('viewed/<int:pk>', ViewedProducts.as_view(), name='viewed'),
    path('catalog/price/', CatalogSortPrice.as_view(), name='sortPrice'),
    path('catalog/pricemax/', CatalogSortPriceMax.as_view(), name='sortPriceMax'),
    path('catalog/review/', CatalogSortReview.as_view(), name='sortReview'),
    path('catalog/new/', CatalogSortNew.as_view(), name='sortNew'),
    path('catalog/search/', SearchProduct.as_view(), name='searchProduct'),
    path('catalog/searchfilter/', SearchFilter.as_view(), name='searchFilter')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
