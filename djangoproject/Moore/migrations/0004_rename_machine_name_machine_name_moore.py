# Generated by Django 4.2 on 2023-04-07 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Moore", "0003_machine_name_remove_moore_unique_name_moore_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Machine_name",
            new_name="Machine_name_Moore",
        ),
    ]
