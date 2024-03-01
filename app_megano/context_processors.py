from cart.services.cart import Cart
from orders.services.orderInfo import OrderInfo


def cart(request):
    return {'cart': Cart(request)}


def load_order(request):
    order = OrderInfo(request)
    if list(order):
        return {'order': list(order)[0]}
    return []
