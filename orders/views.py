from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponse, HttpRequest

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from app_users.models import CustomUser
from orders.forms import OrderForms, NumberCard
from orders.models import Order
from orders.services.orderInfo import OrderInfo
from orders.services.payment import (
    add_order,
    add_detail_to_order,
    get_number_card
)


class OrderView(TemplateView):
    """Страница с оформлением заказа."""

    template_name: str = "orders/order.html"

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data()
        user: CustomUser = self.request.user
        form: OrderForms = OrderForms()
        form_login: AuthenticationForm = AuthenticationForm()

        if hasattr(user, "profile"):
            form = OrderForms(
                {
                    "full_name": f"{user.last_name} {user.first_name} "
                                 f"{user.profile.patronymic}",
                    "email": user.email,
                    "phone": user.profile.phone,
                    "type_delivery": "simple",
                    "type_payment": "cart",
                }
            )
        context.update({"form": form, "form2": form_login})
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        form: OrderForms = OrderForms(request.POST)
        user: CustomUser = self.request.user
        order_info: OrderInfo = OrderInfo(request)

        if form.is_valid():
            order, payment = add_order(
                form, user, order_info.get_total_price()
            )
            add_detail_to_order(order, request)

            if payment == "cart":
                return redirect(reverse("payment", args=[order.pk]))

            elif payment == "random":
                return redirect(
                    reverse("paymentSomeOne", args=[order.pk])
                )
        return render(
            request, "orders/order.html", {"form": form}
        )


def add_info_about_user(request: HttpRequest) -> JsonResponse:
    """
    Получает форму с данными о заказе и отправляет на сохранение в сессии.
    """
    if request.method == "POST":
        form = OrderForms(request.POST)

        if form.is_valid():
            order_info = OrderInfo(request)
            order_info.add(form=form, request=request)
            return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def login_modal(request: HttpRequest) -> HttpResponse:
    """
    Обрабатываем запрос на авторизацию из всплывающего окна при оформлении
    заказа, если авторизация прошла успешно то продолжаем оформление,
    если нет то отправляем на страницу login.html.
    """
    form: AuthenticationForm = AuthenticationForm(data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            email: str = form.cleaned_data.get("username")
            password: str = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("order")

    form.add_error("username", "Пользователь не найден((")
    return render(
        request, "app_users/login.html", {"form": form}
    )


class PaymentView(DetailView):
    """Страница с вводом номера карты пользователя."""

    template_name: str = "orders/payment.html"
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        form: NumberCard = NumberCard()
        context.update({"header": "Оплата со своей карты", "form": form})
        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        form: NumberCard = NumberCard(request.POST)
        order: Order = Order.objects.get(id=pk)

        if form.is_valid():
            get_number_card(form, order)
            return redirect(reverse("progressPayment"))

        return render(
            request,
            "orders/paymentSomeOne.html",
            {"header": "Оплата с карты", "form": form},
        )


class PaymentSomeOneView(DetailView):
    """Страница с вводом случайно выбранного номера карты."""

    template_name: str = "orders/paymentSomeOne.html"
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляет идентификатор для отображения сортировки в шаблоне."""
        context: dict = super().get_context_data()
        form: NumberCard = NumberCard()
        context.update({"header": "Оплата с чужой карты", "form": form})
        return context

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        form: NumberCard = NumberCard(request.POST)
        order: Order = Order.objects.get(id=pk)
        if form.is_valid():
            get_number_card(form, order)
            return redirect(reverse("progressPayment"))

        return render(
            request,
            "orders/paymentSomeOne.html",
            {"header": "Оплата с чужой карты", "form": form},
        )


class ProgressPaymentView(TemplateView):
    """Страница с фиктивной оплатой товара."""

    template_name: str = "orders/progressPayment.html"

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляем header для отображения названия страницы."""
        context: dict = super().get_context_data()
        context.update({"header": "Прогресс оплаты"})
        return context


class OneOrderView(DetailView):
    """Страница с подробной информацией о заказе."""

    template_name: str = "orders/oneOrder.html"
    model = Order

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data()
        obj: Order = self.object

        # Для того чтобы отправить на оплату своей картой или случайной
        link = True
        if obj.type_payment == "random":
            link = False

        # Проверяем есть ли комментарий у заказа
        if obj.comment:
            context.update({"statuses": True})

        context.update({"link": link, "header": "Информация о заказе."})
        return context
