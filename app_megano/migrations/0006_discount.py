# Generated by Django 4.1.3 on 2023-02-19 19:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_megano", "0005_alter_tags_options_alter_tags_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("valid_from", models.DateTimeField(verbose_name="Начало акции")),
                ("valid_to", models.DateTimeField(verbose_name="Конец акции")),
                (
                    "discount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="Скидка в %",
                    ),
                ),
                ("active", models.BooleanField(verbose_name="Активность")),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discounts",
                        to="app_megano.goods",
                        verbose_name="Товар",
                    ),
                ),
            ],
        ),
    ]
