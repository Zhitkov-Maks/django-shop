from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CartView, AddProduct, DeleteProduct, AddProductQuantity, RemoveProductQuantity

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('add/<int:pk>', AddProduct.as_view(), name='add'),
    path('delete/<int:pk>', DeleteProduct.as_view(), name='delete'),
    path('addQuantity/<int:pk>', AddProductQuantity.as_view(), name='quantityAdd'),
    path('removeQuantity/<int:pk>', RemoveProductQuantity.as_view(), name='quantityRemove')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
