# Generated by Django 4.1.3 on 2022-12-27 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logotype', models.FileField(default=0, upload_to='files/logo', verbose_name='Логотип')),
                ('phone', models.CharField(default=0, max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(default=0, max_length=50, verbose_name='Email')),
                ('skype', models.CharField(default=0, max_length=50, verbose_name='Skype')),
                ('address', models.CharField(default=0, max_length=200, verbose_name='Адрес')),
                ('price_delivery_express', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Стоимость экспресс доставки')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Стоимость обычной доставки')),
                ('min_sum', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Минимальная сумма для бесплатной доставки')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]