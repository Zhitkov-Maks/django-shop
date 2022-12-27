from django.views.generic import ListView

from app_megano.models import Goods


class CartView(ListView):
    model = Goods
    template_name = 'cart/cart.html'
