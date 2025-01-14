# Generated by Django 5.1.4 on 2025-01-13 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_settings', '0002_alter_sitesettings_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.CharField(blank=True, max_length=200, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='email',
            field=models.EmailField(blank=True, max_length=50, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='logotype',
            field=models.FileField(blank=True, null=True, upload_to='files/logo', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='skype',
            field=models.CharField(blank=True, max_length=50, verbose_name='Skype'),
        ),
    ]