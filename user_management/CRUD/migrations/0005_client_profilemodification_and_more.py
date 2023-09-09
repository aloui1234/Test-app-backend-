# Generated by Django 4.1.7 on 2023-09-06 21:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CRUD", "0004_employee_profilemodification"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="profilemodification",
            field=models.ManyToManyField(
                null=True,
                related_name="clientmodification",
                to="CRUD.profilemodification",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="profilemodification",
            field=models.ManyToManyField(
                null=True,
                related_name="employeemodification",
                to="CRUD.profilemodification",
            ),
        ),
    ]