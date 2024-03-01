# Generated by Django 4.1.3 on 2023-02-10 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_megano', '0003_goods_free_delivery_goods_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('date_purchases', models.DateTimeField(auto_now=True)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipments', to='app_megano.goods', verbose_name='Товар')),
            ],
        ),
    ]