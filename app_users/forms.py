from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, CharField, ImageField

from .models import CustomUser, Profile


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    password1: CharField = forms.CharField(
        label="Пароль", widget=forms.PasswordInput()
    )
    password2: CharField = forms.CharField(
        label="Повторите пароль", widget=forms.PasswordInput()
    )
    email: EmailField = forms.EmailField(label="Ваш email")
    first_name: CharField = forms.CharField(label="Имя")
    last_name: CharField = forms.CharField(label="Фамилия")
    phone: CharField = forms.CharField(label="Телефон")
    patronymic: CharField = forms.CharField(label="Отчество")

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "phone",
            "password1",
            "password2",
        ]

    def clean_email(self) -> str:
        """
        Метод для проверки существования email в базе данных.
        Если существует, то добавляем сообщение об ошибке."""
        email: str = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_phone(self) -> str:
        """
        Метод для проверки существования телефона в базе данных.
        Если существует, то добавляем сообщение об ошибке.
        """
        phone: str = self.cleaned_data.get("phone")
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Номер телефона уже занят!")
        return phone

    def clean_password2(self) -> str:
        """
        Метод для проверки совпадения паролей в форме. Если не совпадают,
        то добавляем сообщение об ошибке.
        """
        password2: str = self.cleaned_data.get("password2")
        if password2 != self.cleaned_data.get("password1"):
            raise forms.ValidationError("Пароли не совпадают!")
        return password2


def file_size(value) -> None:
    """
    Функция для проверки на размер загружаемого файла на аватар,
    файл не должен превышать 2 Мб.
    """
    limit: int = 2 * 1024 * 1024
    if value.size > limit:
        raise forms.ValidationError("Файл не должен быть больше 2 MB.")


class UpdateUserForm(forms.Form):
    """Форма для обновления данных в профиле."""

    avatar: ImageField = forms.ImageField(
        label="Выберите аватар",
        required=False,
        validators=[file_size],
        widget=forms.FileInput(
            attrs={
                "class": "Profile-file form-input",
                "id": "avatar",
                "name": "avatar",
                "type": "file",
                "data-validate": "onlyImgAvatar",
            }
        ),
    )
    full_name: CharField = forms.CharField(
        max_length=50,
        label="ФИО",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    phone: CharField = forms.CharField(
        max_length=12,
        label="Телефон",
        widget=forms.TextInput(attrs={"class": "form-label"}),
    )
    email: CharField = forms.CharField(
        max_length=30,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-label"}),
    )
    password: CharField = forms.CharField(
        max_length=30,
        label="Пароль",
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-label", "placeholder": "Изменить пароль"}
        ),
    )
    passwordReplay: CharField = forms.CharField(
        max_length=30,
        label="Повторите пароль",
        required=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-label", "placeholder": "Повторите пароль"}
        ),
    )
