from django.urls import path

from .views import (
    ProgressPaymentView,
    PaymentSomeOneView,
    PaymentView,
    OrderView,
    OneOrderView,
    login_modal,
    add_info_about_user,
)

urlpatterns = [
    path("", OrderView.as_view(), name="order"),
    path("payment/<int:pk>/", PaymentView.as_view(), name="payment"),
    path(
        "paymentsomeone/<int:pk>/", PaymentSomeOneView.as_view(), name="paymentSomeOne"
    ),
    path("progresspayment/", ProgressPaymentView.as_view(), name="progressPayment"),
    path("oneorder/<int:pk>", OneOrderView.as_view(), name="oneOrder"),
    path("modalLogin/", login_modal, name="modalLogin"),
    path("addInfoUser/", add_info_about_user, name="addInfo"),
]
