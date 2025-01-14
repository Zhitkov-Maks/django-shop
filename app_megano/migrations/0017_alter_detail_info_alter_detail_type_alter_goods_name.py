# Generated by Django 5.1.4 on 2025-01-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0016_alter_goods_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='info',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='type',
            field=models.CharField(db_index=True, max_length=40, verbose_name='Название атрибута'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
    ]
