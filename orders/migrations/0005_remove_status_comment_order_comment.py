# Generated by Django 4.1.3 on 2023-03-13 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='comment',
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(max_length=100, null=True, verbose_name='Комментарий'),
        ),
    ]
