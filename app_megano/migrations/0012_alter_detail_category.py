# Generated by Django 4.1.3 on 2023-03-19 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0011_detail_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='category',
            field=models.ManyToManyField(to='app_megano.category', verbose_name='Категория'),
        ),
    ]