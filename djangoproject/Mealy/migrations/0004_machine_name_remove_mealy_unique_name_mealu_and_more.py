# Generated by Django 4.2 on 2023-04-07 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Mealy", "0003_remove_mealy_unique_name_mealy_unique_name_mealu"),
    ]

    operations = [
        migrations.CreateModel(
            name="Machine_name",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="mealy",
            name="unique_name_Mealu",
        ),
        migrations.AddConstraint(
            model_name="machine_name",
            constraint=models.UniqueConstraint(
                fields=("name",), name="unique_name_Mealy"
            ),
        ),
        migrations.AlterField(
            model_name="mealy",
            name="name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Mealy.machine_name"
            ),
        ),
    ]
