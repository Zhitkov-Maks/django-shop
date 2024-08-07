# Generated by Django 4.1.3 on 2023-01-31 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_megano", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="goods",
            name="free_delivery",
            field=models.BooleanField(
                default=False, verbose_name="Бесплатная доставка"
            ),
        ),
        migrations.AddField(
            model_name="goods",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активен"),
        ),
    ]
