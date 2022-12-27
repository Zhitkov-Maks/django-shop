from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import RegisterUserForm, UpdateUserForm
from .services import edit_profile


class RegisterUser(CreateView):
    """Класс реализует регистрацию пользователей."""
    form_class = RegisterUserForm
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'app_users/register.html', {'form': form})


def validate_username(request):
    """Проверка доступности логина"""
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists(),
        'is_email': User.objects.filter(email=email).exists()
    }
    return JsonResponse(response)


class LoginUser(LoginView):
    """Класс реализует аутентификацию пользователей."""
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('catalog')


class LogoutUser(LogoutView):
    next_page = 'home'


class AccountView(View):
    def get(self, request):
        user = self.request.user
        if user.users.exists():
            order = user.users.latest('order_date')
            return render(request, 'app_users/account.html', {'order': order})
        return render(request, 'app_users/account.html')


class ProfileView(View):
    def get(self, request):
        user = self.request.user
        form = UpdateUserForm()
        if hasattr(user, 'profile'):
            form = UpdateUserForm(
                {
                    'avatar': user.profile.photo,
                    'email': user.email,
                    'phone': user.profile.phone,
                    'full_name': f'{user.last_name} {user.first_name} {user.profile.patronymic}'
                }
            )
        return render(request, 'app_users/profile.html', {'form': form})

    def post(self, request):
        form = UpdateUserForm(request.POST, request.FILES)
        user = self.request.user
        if form.is_valid() and len(form.cleaned_data['full_name'].split()) == 3:
            edit_profile(user, form)
            return redirect(reverse('login'))
        return render(request, 'app_users/profile.html', context={'form': form})


class HistoryOrderView(ListView):
    model = User
    template_name = 'app_users/historyorder.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return user.users.all().order_by('-order_date')

