# Generated by Django 4.1.3 on 2023-02-25 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_confirmed_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detailorder',
            options={'verbose_name': 'единица заказа', 'verbose_name_plural': 'детали заказа'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='confirmed_order',
        ),
    ]
