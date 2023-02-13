from django.urls import path

from .views import ProgressPaymentView, PaymentSomeOneView, PaymentView, OrderView, OneOrderView, login_modal, \
    check_form

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('paymentsomeone/', PaymentSomeOneView.as_view(), name='paymentsomeone'),
    path('progresspayment/', ProgressPaymentView.as_view(), name='progresspayment'),
    path('oneorder/<int:pk>', OneOrderView.as_view(), name='oneorder'),
    path('modalLogin', login_modal, name='modalLogin'),
    path('check_form/', check_form, name='check_form')
]
