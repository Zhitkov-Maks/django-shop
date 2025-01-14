from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app_megano.views.view import (
    HomeView,
    ShowCategory,
    ProductDetailView,
    ShowTag,
    ViewedProducts, Sale
)
from app_megano.views.views_sort_and_search import (
    CatalogSortView,
    SearchProduct,
    SearchFilter
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "goods/categories/<int:pk>/",
        ShowCategory.as_view(),
        name="category"
    ),
    path("goods/tags/<int:pk>/", ShowTag.as_view(), name="tag"),
    path(
        "goods/detail/<int:pk>",
        ProductDetailView.as_view(),
        name="detail"
    ),
    path(
        "goods/viewed/<int:pk>",
        ViewedProducts.as_view(),
        name="viewed"
    ),
    path(
        "goods/catalog/",
        CatalogSortView.as_view(),
        name="catalog"
    ),
    path(
        "goods/catalog/search/",
        SearchProduct.as_view(),
        name="searchProduct"
    ),
    path(
        "goods/catalog/searchfilter/",
        SearchFilter.as_view(),
        name="searchFilter"
    ),
    path("goods/sale/", Sale.as_view(), name="sale"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
