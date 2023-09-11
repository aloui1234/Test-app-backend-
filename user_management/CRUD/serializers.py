from rest_framework import serializers
from .models import Employee, Client,User, Role, Permission, Plan, Profile, Company, ProfileModification


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        role = Role.objects.create(**validated_data)
        role.permissions.set(permissions)
        return role


class ProfileSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    class Meta:
        model = Profile
        fields = '__all__'
    
    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    

class ProfileModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModification
        fields = '__all__'  


class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = (
            'user',
            'role',
            'company'
        )

    def create(self, validated_data):
        # Create User instance
        user = User.objects.create_user(**validated_data['user'])
        user.save()
        # Create Employee instance
        role = Role.objects.get(id=validated_data['role'].id)
        companyName = self.context.get('companyName')
        company = Company.objects.get(company_name=companyName)
        employee = Employee.objects.create(user=user, role=role, company=company)
        return employee


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = (
            'user',
        )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "company_name",
            "clients",
            "created_date",
        )