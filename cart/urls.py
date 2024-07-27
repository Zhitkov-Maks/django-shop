from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CartView,
    add_product,
    delete_product,
    remove_product_quantity
)

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>", add_product, name="add"),
    path("delete/<int:pk>", delete_product, name="delete"),
    path(
        "removeQuantity/<int:pk>",
        remove_product_quantity,
        name="quantityRemove"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
