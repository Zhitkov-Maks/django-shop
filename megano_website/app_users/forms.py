from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Profile


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
    email = forms.EmailField(label='Ваш email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    phone = forms.CharField(label='Телефон')
    patronymic = forms.CharField(label='Отчество')

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'patronymic', 'phone', 'password1', 'password2']

    def clean_email(self):
        """Метод для проверки существования email в базе данных. Если существует, то добавляем сообщение об ошибке"""
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email

    def clean_phone(self):
        """Метод для проверки существования телефона в базе данных. Если существует, то добавляем сообщение об ошибке"""
        phone = self.cleaned_data.get('phone')
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Номер телефона уже занят!')
        return phone

    def clean_password2(self):
        """Метод для проверки совпадения паролей в форме. Если не совпадают, то добавляем сообщение об ошибке"""
        password2 = self.cleaned_data.get('password2')
        if password2 != self.cleaned_data.get('password1'):
            raise forms.ValidationError('Пароли не совпадают!')
        return password2


def file_size(value):
    """Функция для проверки на размер загружаемого файла на аватар, файл не должен превышать 2 Мб."""
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise forms.ValidationError('Файл не должен быть больше 2 MB.')


class UpdateUserForm(forms.Form):
    """Форма для обновления данных в профиле."""
    avatar = forms.ImageField(label='Выберите аватар', required=False, validators=[file_size],
                              widget=forms.FileInput(attrs={'class': 'Profile-file form-input',
                                                            'id': 'avatar', 'name': 'avatar',
                                                            'type': 'file',
                                                            'data-validate': 'onlyImgAvatar'}))
    full_name = forms.CharField(max_length=50, label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=12, label='Телефон', widget=forms.TextInput(attrs={'class': 'form-label'}))
    email = forms.CharField(max_length=30, label='Email', widget=forms.EmailInput(attrs={'class': 'form-label'}))
    password = forms.CharField(max_length=30, label='Пароль', required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-label',
                                                                 'placeholder': 'Изменить пароль'}))
    passwordReplay = forms.CharField(max_length=30, label='Повторите пароль', required=False,
                                     widget=forms.PasswordInput(attrs={'class': 'form-label',
                                                                       'placeholder': 'Повторите пароль'}))
