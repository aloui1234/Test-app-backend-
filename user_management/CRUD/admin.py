from django.contrib import admin

# Register your models here.
from . import models


class PermissionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'permission_name',
    )


class PermissionGroupAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'permission_group_name',
    )


class RoleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'role_name',
    )


class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'password',
        'last_login',
        'user_id',
        'username',
        'email',
        'username',
        'first_name',
        'last_name',
        'date_joined',
        'is_active',
        'is_recognized',
        'is_staff',
        'is_superuser',
        'is_deleted',
        'created_date',
        'modified_date',
        'created_by',
        'modified_by',
    )
    list_filter = (
        'email',
        'username',
        'first_name',
        'last_name', 
        'is_superuser'       
    )
    

class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role'
    )
    list_filter = (
        'user',
        'role'       
    )
    raw_id_fields = ('user','role')


class ClientAdmin(admin.ModelAdmin):

    list_display = (
        'user',
    )
    list_filter = (
        'user',      
    )
    raw_id_fields = ('user',)


def register_models(admin_class_list):
    for model, admin_class in admin_class_list:
        admin.site.register(model, admin_class)

register_models([
    (models.Permission, PermissionAdmin),
    (models.PermissionGroup, PermissionGroupAdmin),
    (models.Role, RoleAdmin),
    (models.User, UserAdmin),
    (models.Employee, EmployeeAdmin),
    (models.Client, ClientAdmin),
])