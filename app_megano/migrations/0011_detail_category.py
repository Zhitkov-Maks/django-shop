# Generated by Django 4.1.3 on 2023-03-19 15:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_megano", "0010_alter_comment_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="detail",
            name="category",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="app_megano.category",
                verbose_name="Категория",
            ),
        ),
    ]
