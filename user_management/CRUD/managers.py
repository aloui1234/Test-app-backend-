from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.apps import apps

class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, email, password, role=None, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
         
        email = self.normalize_email(email)

        if role:
            extra_fields['role'] = role

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create a Superuser object
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    