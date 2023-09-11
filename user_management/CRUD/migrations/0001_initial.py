# Generated by Django 3.2.9 on 2023-09-11 07:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('iban', models.CharField(max_length=30)),
                ('swift_code', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('clients', models.ManyToManyField(related_name='clients', to='CRUD.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_profile', to='CRUD.company')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(default='', max_length=30)),
                ('backup_email', models.EmailField(blank=True, max_length=254)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_recognized', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.EmailField(default='system', max_length=254)),
                ('modified_by', models.EmailField(default='system', max_length=254)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=50)),
                ('permissions', models.ManyToManyField(to='CRUD.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Modification Date')),
                ('modified_data', models.JSONField(default=dict, null=True, verbose_name='Modified Data')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_modifications_created', to='CRUD.role', verbose_name='Modified By')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_modifications', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'profile modification',
                'verbose_name_plural': 'profile modifications',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('job_title', models.CharField(default='', max_length=100)),
                ('date_of_birth', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('avatar', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(default='', max_length=100)),
                ('language', models.CharField(default='', max_length=100)),
                ('skype', models.CharField(default='', max_length=100)),
                ('status', models.CharField(choices=[('option1', 'ACTIVE'), ('option2', 'IN MEETING'), ('option3', 'ABSENT'), ('option4', 'OFFLINE'), ('option5', 'AWAY'), ('option6', 'BLOCKED'), ('option7', 'DISABLED')], default='option1', max_length=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to='CRUD.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=50, unique=True)),
                ('max_number_members', models.IntegerField()),
                ('cloud_storage', models.IntegerField()),
                ('apps', models.ManyToManyField(related_name='related_apps', to='CRUD.App')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_group_name', models.CharField(max_length=50, unique=True)),
                ('permissions', models.ManyToManyField(to='CRUD.Permission')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='profilemodification',
            field=models.ManyToManyField(null=True, related_name='employeemodification', to='CRUD.ProfileModification'),
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_role', to='CRUD.role'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='CRUD.plan'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'candidate',
                'verbose_name_plural': 'candidates',
            },
        ),
    ]
