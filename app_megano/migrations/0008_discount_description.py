# Generated by Django 4.1.3 on 2023-02-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_megano", "0007_alter_discount_options_alter_discount_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="discount",
            name="description",
            field=models.TextField(
                default=0, max_length=200, verbose_name="Описание скидки"
            ),
            preserve_default=False,
        ),
    ]
