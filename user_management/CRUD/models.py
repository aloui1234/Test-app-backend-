from django.db import models

import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

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
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  date_of_birth = models.DateTimeField(default=timezone.now)
  backup_email = models.EmailField(blank=True)
  phone_number = models.CharField(max_length=20, blank=True)
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


class Employee(models.Model):
  """
    User subtype with specific fields and properties
    """
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, related_name='user_role', null=True)
  
  class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'


class Client(models.Model):
  """
    User subtype with specific fields and properties
    """
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
  
  class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'






  
