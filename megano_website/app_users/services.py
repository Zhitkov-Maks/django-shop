from django.contrib.auth import authenticate, login

from .models import Profile, CustomUser


def func_for_check_form(form, user, request):
    """Проверяем форму и сохраняем данные из формы"""
    edit_email(user, form.cleaned_data.get('email'), form)
    user.first_name = form.cleaned_data.get('full_name').split()[1]
    user.last_name = form.cleaned_data.get('full_name').split()[0]

    if hasattr(user, 'profile'):
        edit_phone(user, form.cleaned_data.get('phone'), form)
        if form.cleaned_data.get('avatar'):
            user.profile.photo = form.cleaned_data.get('avatar')
        user.profile.patronymic = form.cleaned_data.get('full_name').split()[2]
        user.profile.save()

    else:
        Profile.objects.create(
            user=user,
            patronymic=form.cleaned_data['full_name'].split()[-1],
            photo=form.cleaned_data['avatar'],
            phone=form.cleaned_data['phone']
        )
    if form.cleaned_data.get('password') and form.cleaned_data.get('passwordReplay'):
        if form.cleaned_data['password'] == form.cleaned_data['passwordReplay']:
            user.set_password(form.cleaned_data['password'])
            email = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_pass)
            login(request, user)
        else:
            form.add_error('passwordReplay', 'Пароли не совпадают.')
            form['passwordReplay'].field.widget.attrs['class'] += ' form-input_error'
            return False
    user.save()
    if form.is_valid():
        return True
    return False


def edit_email(user, email, form):
    """Функция для сохранения email, если пользователь хочет сменить email проверяем не используется ли уже данная
    почта."""
    if email != user.email:
        if CustomUser.objects.filter(email=email).exists():
            form.add_error('email', 'Данный email уже используется')
            form['email'].field.widget.attrs['class'] += ' form-input_error'
        else:
            user.email = email
            user.save()


def edit_phone(user, phone, form):
    """Функция для проверки и сохранения измененного номера телефона."""
    if phone != user.profile.phone:
        if Profile.objects.filter(phone=phone).exists():
            form.add_error('phone', 'Этот телефон уже используется')
            form['phone'].field.widget.attrs['class'] += ' form-input_error'
        else:
            user.profile.phone = phone
            user.profile.save()
