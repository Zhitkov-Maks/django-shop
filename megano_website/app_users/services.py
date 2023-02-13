from .models import Profile


def edit_profile(user, form):
    try:
        if form.cleaned_data['password'] and form.cleaned_data['passwordReplay']:
            if form.cleaned_data['password'] == form.cleaned_data['passwordReplay']:
                user.set_password(form.cleaned_data['password'])
            else:
                form.add_error('passwordReplay', 'Пароли не совпадают.')
                return False
        user.first_name = form.cleaned_data['full_name'].split()[1]
        user.last_name = form.cleaned_data['full_name'].split()[0]
        if hasattr(user, 'profile'):
            user.profile.photo = form.cleaned_data['avatar']
            user.profile.patronymic = form.cleaned_data['full_name'].split()[-1]
            user.profile.save()
        else:
            Profile.objects.create(
                user=user,
                patronymic=form.cleaned_data['full_name'].split()[-1],
                photo=form.cleaned_data['avatar'],
                phone=form.cleaned_data['phone']
            )
        user.save()
        return True
    except TypeError:
        return False
