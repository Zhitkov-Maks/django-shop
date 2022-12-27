from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        """Метод для проверки существования email в базе данных. Если существует до добавляем сообщение об ошибке"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use')
        return email


class UpdateUserForm(forms.Form):
    avatar = forms.ImageField(label='Выберите аватар', widget=forms.FileInput(attrs={'class': 'Profile-file form-input',
                                                                                     'id': 'avatar', 'name': 'avatar',
                                                                                     'type': 'file',
                                                                                     'data-validate': 'onlyImgAvatar'}))
    full_name = forms.CharField(max_length=50, label='ФИО', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=12, label='Телефон', widget=forms.TextInput(attrs={'class': 'form-label'}))
    email = forms.CharField(max_length=30, label='Email', widget=forms.EmailInput(attrs={'class': 'form-label'}))
    password = forms.CharField(max_length=30, label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-label'}))
    passwordReplay = forms.CharField(max_length=30, label='Повторите пароль',
                                     widget=forms.PasswordInput(attrs={'class': 'form-label'}))
