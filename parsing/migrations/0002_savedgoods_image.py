# Generated by Django 5.1.1 on 2024-10-11 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parsing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="savedgoods",
            name="image",
            field=models.CharField(
                db_index=True,
                default="https://st4.depositphotos.com/14953852/22772/v/450/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg",
                max_length=600,
            ),
        ),
    ]
