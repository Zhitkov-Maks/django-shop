from django.urls import path

from .views import ProgressPaymentView, PaymentSomeOneView, PaymentView, OrderView, OneOrderView

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('paymentsomeone/', PaymentSomeOneView.as_view(), name='paymentsomeone'),
    path('progresspayment/', ProgressPaymentView.as_view(), name='progresspayment'),
    path('oneorder/<int:pk>', OneOrderView.as_view(), name='oneorder'),
]
