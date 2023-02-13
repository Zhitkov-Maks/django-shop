from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView

from orders.forms import OrderForms
from orders.models import DetailOrder, Order
from orders.services.payment import add_order, add_detail_to_order
from cart.services.cart import Cart


class OrderView(TemplateView):
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        form = OrderForms()
        form_login = AuthenticationForm()
        if hasattr(user, 'profile'):
            form = OrderForms({
                'full_name': f'{user.first_name} {user.last_name} {user.profile.patronymic}',
                'email': user.email,
                'phone': user.profile.phone
            })
        context.update({'form': form, 'form2': form_login})
        return context

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


def check_form(request, *args, **kwargs):
    form = OrderForms(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, 'orders/order.html', {'form': form})


def login_modal(request):
    """Обрабатываем запрос на авторизацию из всплывающего окна при оформлении заказа, если авторизация прошла
    успешно то продолжаем оформление, если нет то отправляем на страницу login.html"""
    form = AuthenticationForm(data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('order')
    form.add_error('username', 'Пользователь не найден((')
    return render(request, 'app_users/login.html', {'form': form})


class PaymentView(TemplateView):
    template_name = 'orders/payment.html'


class PaymentSomeOneView(TemplateView):
    template_name = 'orders/paymentsomeone.html'


class ProgressPaymentView(TemplateView):
    template_name = 'orders/progressPayment.html'


class OneOrderView(DetailView):
    template_name = 'orders/oneorder.html'
    model = Order
