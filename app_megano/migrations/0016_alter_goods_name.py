# Generated by Django 4.1.7 on 2024-02-07 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0015_remove_detail_category_alter_goods_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
    ]