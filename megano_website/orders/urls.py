from django.urls import path

from .views import ProgressPaymentView, PaymentSomeOneView, PaymentView, OrderView, OneorderView

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('paymentsomeone/', PaymentSomeOneView.as_view(), name='paymentsomeone'),
    path('progresspayment/', ProgressPaymentView.as_view(), name='progresspayment'),
    path('oneorder/', OneorderView.as_view(), name='oneorder'),
]
