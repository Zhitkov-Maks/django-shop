from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, CatalogView, ShowCategory, ProductDetailView, ShowTag, ViewedProducts, \
    CatalogSortPrice, CatalogSortReview, CatalogSortNew, CatalogSortPriceMax, SearchProduct, SearchFilter, Sale, \
    CatalogSortOld, CatalogSortReviewMin

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('goods/catalog/', CatalogView.as_view(), name='catalog'),
    path('goods/categories/<int:pk>/', ShowCategory.as_view(), name="category"),
    path('goods/tags/<int:pk>/', ShowTag.as_view(), name="tag"),
    path('goods/detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('goods/viewed/<int:pk>', ViewedProducts.as_view(), name='viewed'),
    path('goods/catalog/price/', CatalogSortPrice.as_view(), name='sortPrice'),
    path('goods/catalog/pricemax/', CatalogSortPriceMax.as_view(), name='sortPriceMax'),
    path('goods/catalog/review/', CatalogSortReview.as_view(), name='sortReview'),
    path('goods/catalog/reviewMin/', CatalogSortReviewMin.as_view(), name='sortReviewMin'),
    path('goods/catalog/new/', CatalogSortNew.as_view(), name='sortNew'),
    path('goods/catalog/old/', CatalogSortOld.as_view(), name='sortOld'),
    path('goods/catalog/search/', SearchProduct.as_view(), name='searchProduct'),
    path('goods/catalog/searchfilter/', SearchFilter.as_view(), name='searchFilter'),
    path('goods/sale/', Sale.as_view(), name='sale'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
