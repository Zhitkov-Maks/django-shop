# from django.contrib.auth.models import User
# from django.db import models
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
#     patronymic = models.CharField(max_length=20, verbose_name='Отчество')
#     photo = models.ImageField(upload_to='files/image', verbose_name='Фото', blank=True)
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#
#     def __str__(self):
#         return str(self.user)
#
#     class Meta:
#         verbose_name = 'пользователь'
#         verbose_name_plural = 'пользователи'
