"""Все нижепредставленные классы для тестирования шаблонов."""

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterUserForm


class RegisterUser(CreateView):
    """Класс реализует регистрацию пользователей."""
    form_class = RegisterUserForm
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('home')


class LoginUser(LoginView):
    """Класс реализует аутентификацию пользователей."""
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = 'home'


class AccountView(View):
    def get(self, request):
        return render(request, 'app_users/account.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'app_users/profile.html')


class HistoryOrderView(View):
    def get(self, request):
        return render(request, 'app_users/historyorder.html')
