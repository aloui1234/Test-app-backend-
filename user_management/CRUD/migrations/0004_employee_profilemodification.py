# Generated by Django 4.1.7 on 2023-09-06 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CRUD", "0003_alter_employee_options_profilemodification"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="profilemodification",
            field=models.ManyToManyField(
                related_name="profilemodification", to="CRUD.profilemodification"
            ),
        ),
    ]
