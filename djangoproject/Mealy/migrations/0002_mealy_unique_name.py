# Generated by Django 4.2 on 2023-04-07 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Mealy", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="mealy",
            constraint=models.UniqueConstraint(fields=("name",), name="unique_name"),
        ),
    ]