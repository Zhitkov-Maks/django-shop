from django.shortcuts import render
from django.views import View


class OrderView(View):
    def get(self, request):
        return render(request, 'orders/order.html')


class PaymentView(View):
    def get(self, request):
        return render(request, 'orders/payment.html')


class PaymentSomeOneView(View):
    def get(self, request):
        return render(request, 'orders/paymentsomeone.html')


class ProgressPaymentView(View):
    def get(self, request):
        return render(request, 'orders/progressPayment.html')


class OneorderView(View):
    def get(self, request):
        return render(request, 'orders/oneorder.html')
