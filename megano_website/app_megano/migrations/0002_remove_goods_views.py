# Generated by Django 4.1.3 on 2022-12-27 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='views',
        ),
    ]
