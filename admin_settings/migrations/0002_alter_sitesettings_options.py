# Generated by Django 4.1.3 on 2022-12-27 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesettings',
            options={'verbose_name': 'настройки сайта', 'verbose_name_plural': 'настройки сайта'},
        ),
    ]