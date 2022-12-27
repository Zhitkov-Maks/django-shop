from .models import Profile


def edit_profile(user, form):
    user.email = form.cleaned_data['email']
    user.first_name = form.cleaned_data['full_name'].split()[1]
    user.last_name = form.cleaned_data['full_name'].split()[0]
    user.set_password(form.cleaned_data['password'])
    if hasattr(user, 'profile'):
        user.profile.phone = form.cleaned_data['phone']
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
