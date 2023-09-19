from django.db import models

import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth import get_user_model

from .managers import CustomUserManager

# Create your models here.
class Permission(models.Model):
  permission_name = models.CharField(max_length=50, unique=True)

  def __str__(self):
      return self.permission_name


class PermissionGroup(models.Model):
  permission_group_name = models.CharField(max_length=50, unique=True)
  permissions = models.ManyToManyField(Permission)

  def __str__(self):
      return self.permission_group_name


class Role(models.Model):
  role_name = models.CharField(max_length=50)
  permissions = models.ManyToManyField(Permission)

  def __str__(self):
      if self.role_name:
          return self.role_name
      return super().__str__()

 
class User(AbstractBaseUser):
  user_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=30, default='')
  backup_email = models.EmailField(blank=True)
  date_joined = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  is_recognized = models.BooleanField(default=False) 
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_deleted = models.BooleanField(default=False)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  created_by = models.EmailField(default='system')
  modified_by = models.EmailField(default='system')
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
        return self.email
  
  def has_perm(self, perm, obj=None):
    return self.is_superuser

  def has_module_perms(self, app_label):
    return self.is_superuser
  
  class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class ProfileModification(models.Model):
  user = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
    related_name='profile_modifications',
    verbose_name='User'
  )
  modified_by = models.ForeignKey(
    Role,
    on_delete=models.SET_NULL,
    null=True,
    related_name='profile_modifications_created',
    verbose_name='Modified By'
  )
  modified_date = models.DateTimeField(default=timezone.now, verbose_name='Modification Date',null=True)
  modified_data = models.JSONField(default=dict, verbose_name='Modified Data',null=True)

  class Meta:
    verbose_name = 'profile modification'
    verbose_name_plural = 'profile modifications'


class Client(models.Model):
  """
    User subtype with specific fields and properties
    """
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
  
  # New fields for additional client information
  full_name = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  phone_number = models.CharField(max_length=20)
  bank_name = models.CharField(max_length=255)
  country = models.CharField(max_length=255)
  iban = models.CharField(max_length=30)
  swift_code = models.CharField(max_length=30)
  
  class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class App(models.Model):
  app_name = models.CharField(max_length=50, unique=True)

  def __str__(self):
      return self.app_name


class Plan(models.Model):
  plan_name = models.CharField(max_length=50, unique=True)
  max_number_members = models.IntegerField()
  cloud_storage = models.IntegerField()
  apps = models.ManyToManyField(App, related_name='related_apps')

  def __str__(self):
    return self.plan_name


class Company(models.Model):
  company_name = models.CharField(max_length=50, unique=True)
  plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='owner')
  clients = models.ManyToManyField(Client, related_name='clients')
  created_date = models.DateTimeField(default=timezone.now)

  def __str__(self):      
    return self.company_name


class Employee(models.Model):
  """
    User subtype with specific fields and properties
    """
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='user_role', null=True,default=1)
  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_profile')
  profilemodification = models.ManyToManyField(ProfileModification, related_name='employeemodification',null=True)


class Profile(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    job_title = models.CharField(max_length=100, default='')
    date_of_birth = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.CharField(max_length=50, unique=False ,blank=True)
    country = models.CharField(max_length=100, default='')
    language = models.CharField(max_length=100, default='')
    skype = models.CharField(max_length=100, default='')

    OP1 = 'option1'
    OP2 = 'option2'
    OP3 = 'option3'
    OP4 = 'option4'
    OP5 = 'option5'
    OP6 = 'option6'
    OP7 = 'option7'
  
    STATUS_CHOICES = (
      (OP1, 'ACTIVE'),
      (OP2, 'IN MEETING'),
      (OP3, 'ABSENT'),
      (OP4, 'OFFLINE'),
      (OP5, 'AWAY'),
      (OP6, 'BLOCKED'),
      (OP7, 'DISABLED'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OP1)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_profile')

  
    def __str__(self):
      return self.job_title


class Candidate(models.Model):
  """
    User subtype with specific fields and properties
    """
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate')
  
  class Meta:
        verbose_name = 'candidate'
        verbose_name_plural = 'candidates'
  

