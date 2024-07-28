"""
Модуль для проверки введенных данных редактирования профиля, и сохранения.
"""
from django.contrib.auth import authenticate, login
from django.http import HttpRequest

from .forms import UpdateUserForm
from .models import Profile, CustomUser


def update_profile_data(user: CustomUser, form: UpdateUserForm) -> None:
    """Функция для обновления модели профиля."""
    if hasattr(user, "profile"):
        edit_phone(user, form.cleaned_data.get("phone"), form)

        if form.cleaned_data.get("avatar"):
            user.profile.photo = form.cleaned_data.get("avatar")

        user.profile.patronymic = form.cleaned_data.get("full_name").split()[2]
        user.profile.save()

    else:
        Profile.objects.create(
            user=user,
            patronymic=form.cleaned_data["full_name"].split()[-1],
            photo=form.cleaned_data["avatar"],
            phone=form.cleaned_data["phone"],
        )


def update_password(
        user: CustomUser,
        form: UpdateUserForm,
        request: HttpRequest
) -> None:
    """Функция для проверки и сохранения паролей."""
    if form.cleaned_data.get("password") and form.cleaned_data.get(
        "passwordReplay"
    ):
        password = form.cleaned_data.get("password")
        # Если были введены пароли
        if password == form.cleaned_data["passwordReplay"]:

            user.set_password(password)
            user.save()

            # Если смена пароля прошла, то нужно снова авторизоваться
            user = authenticate(
                email=form.cleaned_data.get("email"),
                password=password
            )
            login(request, user)

        else:
            form.add_error("passwordReplay", "Пароли не совпадают.")
            form[
                "passwordReplay"
            ].field.widget.attrs["class"] += ' form-input_error'


def distributor_function(form, user, request) -> bool:
    """
    Проверяем форму и сохраняем данные из формы. Если редактирование прошло
    успешно, то возвращаем True (В конце функции проверяем на is_valid,
    это срабатывает так как при возникновении каких либо ошибок мы
    добавляем к форме add_error), если нет, то False.
    """
    # Сначала отправляем на проверку и сохранение email
    edit_email(user, form.cleaned_data.get("email"), form)

    # Сохраняем имя и фамилию
    user.first_name = form.cleaned_data.get("full_name").split()[1]
    user.last_name = form.cleaned_data.get("full_name").split()[0]

    # Отправляем на обновление данных в профиле
    update_profile_data(user, form)

    # Отправляем на обновление пароля
    update_password(user, form, request)

    # Сохраняем все что обновили
    user.save()

    if form.is_valid():
        return True
    return False


def edit_email(user: CustomUser, email: str, form: UpdateUserForm):
    """
    Функция для сохранения email, если пользователь хочет сменить email
    проверяем не используется ли уже данная почта.
    """
    if email != user.email:
        if CustomUser.objects.filter(email=email).exists():
            form.add_error("email", "Данный email уже используется")
            form[
                "email"
            ].field.widget.attrs["class"] += " form-input_error"

        else:
            user.email = email
            user.save()


def edit_phone(user: CustomUser, phone: str, form: UpdateUserForm):
    """
    Функция для проверки и сохранения измененного номера телефона.
    Проверка на существование введенного телефона.
    """
    if phone != user.profile.phone:
        if Profile.objects.filter(phone=phone).exists():
            form.add_error("phone", "Этот телефон уже используется")
            form[
                "phone"
            ].field.widget.attrs["class"] += " form-input_error"
        else:
            user.profile.phone = phone
            user.profile.save()
