from orders.models import Order, Status, DetailOrder
from cart.services.cart import Cart


def add_order(form, user, total_price):
    order = Order.objects.create(
        full_name=form.cleaned_data['full_name'],
        phone=form.cleaned_data['phone'],
        email=form.cleaned_data['email'],
        city=form.cleaned_data['city'],
        address=form.cleaned_data['address'],
        user_id=user.id,
        type_delivery=form.cleaned_data['type_delivery'],
        type_payment=form.cleaned_data['type_payment'],
        total_price=total_price,
        status=Status.objects.get(pk=1)
    )
    return order


def add_detail_to_order(order, request):
    cart = Cart(request)
    for item in cart:
        DetailOrder.objects.create(order=order,
                                   product=item['product'],
                                   price=item['price'],
                                   quantity=item['quantity'])
    cart.clear()
