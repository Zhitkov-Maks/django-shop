from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView


from app_megano.models import Goods

from cart.services.cart import Cart


class CartView(ListView):
    model = Goods
    template_name = 'cart/cart.html'


class AddProduct(View):
    def get(self, request, pk, quantity=1):
        cart = Cart(request)

        product = get_object_or_404(Goods, id=pk)
        cart.add(
            product=product,
            quantity=quantity
        )
        response = {'success': True}
        return JsonResponse(response)


class DeleteProduct(View):
    def get(self, request, pk):
        cart = Cart(request)

        product = get_object_or_404(Goods, id=pk)
        cart.remove(product=product)
        response = {'success': True}
        return JsonResponse(response)


class AddProductQuantity(View):
    def get(self, request, pk):
        cart = Cart(request)

        product = get_object_or_404(Goods, id=pk)
        cart.add(
            product=product,
            quantity=1
        )
        response = {'success': True}
        return JsonResponse(response)


class RemoveProductQuantity(View):
    def get(self, request, pk):
        cart = Cart(request)

        product = get_object_or_404(Goods, id=pk)
        cart.add(
            product=product,
            quantity=-1
        )
        response = {'success': True}
        for goods in cart:
            if goods['product'] == product:
                if goods['quantity'] <= 0:
                    cart.remove(product=goods['product'])
                    response = {'success': False}
        print(response)
        return JsonResponse(response)
