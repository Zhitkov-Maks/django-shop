from cart.services.cart import Cart
from orders.services.orderInfo import OrderInfo


def cart(request) -> dict:
    """Добавляем в контекст данные о корзине."""
    return {"cart": Cart(request)}


def load_order(request) -> dict | list:
    """
    Добавляем данные о заказе, нужно для вывода введенных пользователем данных.
    """
    order = OrderInfo(request)
    if list(order):
        return {"order": list(order)[0]}
    return []
