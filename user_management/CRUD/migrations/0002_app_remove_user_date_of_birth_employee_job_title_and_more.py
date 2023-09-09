# Generated by Django 4.1.7 on 2023-09-05 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("CRUD", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="App",
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
                ("app_name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="date_of_birth",
        ),
        migrations.AddField(
            model_name="employee",
            name="job_title",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.CreateModel(
            name="Plan",
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
                ("plan_name", models.CharField(max_length=50, unique=True)),
                ("max_number_members", models.IntegerField()),
                ("cloud_storage", models.IntegerField()),
                (
                    "apps",
                    models.ManyToManyField(related_name="related_apps", to="CRUD.app"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Company",
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
                ("company_name", models.CharField(max_length=50, unique=True)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "clients",
                    models.ManyToManyField(related_name="clients", to="CRUD.client"),
                ),
                (
                    "employees",
                    models.ManyToManyField(
                        related_name="employees", to="CRUD.employee"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to="CRUD.employee",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to="CRUD.plan",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Candidate",
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
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "candidate",
                "verbose_name_plural": "candidates",
            },
        ),
    ]
