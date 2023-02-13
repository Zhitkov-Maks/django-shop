from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import RegisterUserForm, UpdateUserForm
from .models import Profile, CustomUser

from .services import edit_profile


class RegisterUser(CreateView):
    """Класс реализует регистрацию пользователей."""
    form_class = RegisterUserForm
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        """Метод проверяет форму и если она валидна сохраняет пользователя в модели CustomUser и дополнительные
        в модели Profile. И так же если сохранение прошло успешно метод аутентифицирует пользователя и авторизует
        пользователя и перенаправляет на главную страницу."""
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            phone = form.cleaned_data.get('phone')
            patronymic = form.cleaned_data.get('patronymic')
            Profile.objects.create(
                user=user,
                phone=phone,
                patronymic=patronymic
            )

            email = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_pass)
            login(request, user)
            return redirect('home')
        return render(request, 'app_users/register.html', {'form': form})


class LoginUser(LoginView):
    """Класс реализует авторизацию пользователей."""
    template_name = 'app_users/login.html'
    success_url = reverse_lazy('home')
    form_class = AuthenticationForm

    def post(self, request, **kwargs):
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(email=username, password=password)
        if user is not None or password is None:
            if user.is_active:
                login(request, user)
                return redirect('home')
        form.add_error('username', 'Неверно введен email или пароль попробуйте еще раз.')
        return render(request, 'app_users/login.html', {'form': form})


class LogoutUser(LogoutView):
    """Класс для выхода пользователя из системы."""
    next_page = 'home'


class AccountView(TemplateView):
    """Класс для отображения профиля пользователя"""
    template_name = 'app_users/account.html'


class ProfileView(TemplateView):
    """Класс для редактирования профиля пользователя."""
    template_name = 'app_users/profile.html'

    def get_context_data(self, **kwargs):
        """Добавляет и вставляет в форму текущие данные пользователя."""
        context = super().get_context_data()
        user = self.request.user
        form = UpdateUserForm()
        if hasattr(user, 'profile'):
            image = user.profile.photo
            context.update({'image': image})
            form = UpdateUserForm(
                {
                    'email': user.email,
                    'phone': user.profile.phone,
                    'full_name': f'{user.last_name} {user.first_name} {user.profile.patronymic}'
                }
            )
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            if email != user.email:  # Проверяем не занята ли почта
                if CustomUser.objects.filter(email=email).exists():
                    form.add_error('email', 'Этот email уже используется.')
                else:
                    user.email = email
            elif phone != user.profile.phone:
                if Profile.objects.filter(phone=phone).exists():
                    form.add_error('phone', 'Этот номер телефона уже занят.')
                else:
                    user.profile.phone = phone
            raw_pass = form.cleaned_data.get('password')
            edit = edit_profile(user, form)
            if raw_pass and edit:
                user = authenticate(email=email, password=raw_pass)
                login(request, user)
        return render(request, 'app_users/profile.html', {'form': form, 'image': user.profile.photo, 'edit': True})


class HistoryOrderView(ListView):
    model = CustomUser
    template_name = 'app_users/historyorder.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        user = CustomUser.objects.get(id=self.kwargs['pk'])
        return user.users.all().order_by('-order_date')
