# Generated by Django 3.2.9 on 2023-09-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD', '0002_auto_20230919_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
