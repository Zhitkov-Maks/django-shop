from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

from orders.forms import OrderForms
from orders.models import DetailOrder, Order
from orders.services.payment import add_order, add_detail_to_order
from cart.services.cart import Cart


class OrderView(View):
    def get(self, request):
        user = self.request.user
        form = OrderForms()
        return render(request, 'orders/order.html', {'form': form})

    def post(self, request):
        form = OrderForms(request.POST)
        user = self.request.user
        cart = Cart(self.request)
        if form.is_valid():
            order = add_order(form, user, cart.get_total_price())
            add_detail_to_order(order, request)
            if form.cleaned_data['type_payment'] == 'A':
                return redirect('payment')
            elif form.cleaned_data['type_payment'] == 'B':
                return redirect('paymentsomeone')
        return render(request, 'orders/order.html', {'form': form})


class PaymentView(View):
    def get(self, request):
        return render(request, 'orders/payment.html')


class PaymentSomeOneView(View):
    def get(self, request):
        return render(request, 'orders/paymentsomeone.html')


class ProgressPaymentView(View):
    def get(self, request):
        return render(request, 'orders/progressPayment.html')


class OneOrderView(DetailView):
    template_name = 'orders/oneorder.html'
    model = Order
