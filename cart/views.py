from django.db.models import PositiveIntegerField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


from app_megano.models import Goods
from app_megano.services import check_product_in_cart

from cart.services.cart import Cart
from orders.services.payment import check_cart


class CartView(ListView):
    """Класс для отображения списка товаров в корзине пользователя."""
    model = Goods
    template_name: str = "cart/cart.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет в контекст корзину."""
        context: dict = super().get_context_data()
        cart = Cart(self.request)
        stock = check_cart(cart)
        context.update({"stock": stock, "header": "Корзина"})
        return context


def add_product(request, pk, quantity=1):
    """Добавляет продукт в корзину."""
    cart: Cart = Cart(request)
    product: Goods = get_object_or_404(Goods, id=pk)

    stock_in_store: PositiveIntegerField = product.stock
    product_true, quantity_in_cart = check_product_in_cart(cart, product)

    if stock_in_store <= quantity_in_cart:
        return JsonResponse({"success": False})

    else:
        cart.add(product=product, quantity=quantity)
        response = {"success": True}
        return JsonResponse(response)


def delete_product(request, pk) -> JsonResponse:
    """Удаляет продукт из корзины."""
    cart = Cart(request)

    product = get_object_or_404(Goods, id=pk)
    cart.remove(product=product)
    response = {"success": True}
    return JsonResponse(response)


def remove_product_quantity(request, pk) -> JsonResponse:
    """Уменьшаем количество выбранного товара в корзине."""
    cart: Cart = Cart(request)

    product: Goods = get_object_or_404(Goods, id=pk)
    cart.add(product=product, quantity=-1)
    response = {"success": True}

    for goods in cart:
        if goods["product"] == product:
            if goods["quantity"] <= 0:
                cart.remove(product=goods["product"])
                response = {"success": False}
    return JsonResponse(response)
