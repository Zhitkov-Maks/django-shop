from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import RegisterUserForm, UpdateUserForm
from .models import Profile, CustomUser

from .services import distributor_function
from orders.models import Order


class RegisterUser(CreateView):
    """Класс реализует регистрацию пользователей."""

    form_class = RegisterUserForm
    template_name: str = "app_users/register.html"
    success_url: str = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Для добавления header."""
        context: dict = super().get_context_data()
        context.update({"header": "Регистрация"})
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Метод проверяет форму и если она валидна сохраняет пользователя
        в модели CustomUser и дополнительные в модели Profile.
        И так же если сохранение прошло успешно метод аутентифицирует
        пользователя и авторизует
        пользователя и перенаправляет на главную страницу.
        """
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            phone = form.cleaned_data.get("phone")
            patronymic = form.cleaned_data.get("patronymic")
            Profile.objects.create(
                user=user, phone=phone, patronymic=patronymic
            )

            email: str = form.cleaned_data.get("email")
            raw_pass: str = form.cleaned_data.get("password1")

            # Аутентифицируем пользователя.
            user = authenticate(email=email, password=raw_pass)
            login(request, user)

            return redirect("home")
        return render(
            request,
            "app_users/register.html",
            {"form": form}
        )


class LoginUser(LoginView):
    """Класс реализует авторизацию пользователей."""

    template_name: str = "app_users/login.html"
    success_url: str = reverse_lazy("home")
    form_class: AuthenticationForm = AuthenticationForm

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """Добавляем header для отображения в строке названия сайта."""
        context: dict = super().get_context_data()
        context.update({"header": "Авторизация"})
        return context

    def post(self, request, **kwargs) -> HttpResponse:
        form: AuthenticationForm = AuthenticationForm(data=request.POST)
        username: str = request.POST["username"]
        password: str = request.POST["password"]

        user = authenticate(email=username, password=password)
        if user is not None or password is None:
            if user.is_active:
                login(request, user)
                return redirect("home")
        form.add_error(
            "username",
            "Неверно введен email или пароль. Попробуйте еще раз."
        )
        return render(
            request, "app_users/login.html", {"form": form}
        )


class LogoutUser(LogoutView):
    """Класс для выхода пользователя из системы."""
    next_page = "home"


class AccountView(LoginRequiredMixin, TemplateView):
    """Класс для отображения профиля пользователя"""

    template_name: str = "app_users/account.html"
    login_url: str = "login"

    def get_context_data(self, **kwargs) -> dict:
        """Получаем последний заказ пользователя, если таковой имеется."""
        context: dict = super().get_context_data()
        user: CustomUser = self.request.user
        if Order.objects.filter(user=user).exists():
            order: Order = Order.objects.filter(user=user).order_by("-id")[0]
            context.update(
                {
                    "order": order,
                    "header": f"Профиль {user.first_name} {user.last_name}",
                }
            )
        return context


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Класс для редактирования профиля пользователя."""

    template_name = "app_users/profile.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        """Добавляет и вставляет в форму текущие данные пользователя."""
        context = super().get_context_data()
        user = self.request.user
        form = UpdateUserForm()
        if hasattr(user, "profile"):  # Проверяем есть ли у нас связь с таблицей profile
            image = user.profile.photo
            context.update({"image": image})
            form = UpdateUserForm(
                {
                    "email": user.email,
                    "phone": user.profile.phone,
                    "full_name": f"{user.last_name} {user.first_name} {user.profile.patronymic}",
                }
            )
        context.update({"form": form, "header": "Редактирование профиля"})
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(request.POST, request.FILES)
        user = request.user
        edit = False
        if form.is_valid():
            if len(form.cleaned_data.get("full_name").split()) == 3:
                edit = distributor_function(form, user, request)
            else:
                form.add_error(
                    "full_name", "Необходимо ввести имя, фамилию и отчество!"
                )
                form["full_name"].field.widget.attrs["class"] += " form-input_error"
        return render(
            request,
            "app_users/profile.html",
            {"form": form, "image": user.profile.photo, "edit": edit},
        )


class HistoryOrderView(LoginRequiredMixin, ListView):
    """Страница для отображения заказов в профиле."""

    model = CustomUser
    template_name = "app_users/historyOrder.html"
    context_object_name = "history_list"
    login_url = "login"

    def get_queryset(self):
        return Order.objects.select_related("status").filter(
            Q(user_id=self.request.user.id)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update({"header": "История заказов"})
        return context
