
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer  # Import your serializer

from django.shortcuts import get_object_or_404, render
from .models import Employee, ProfileModification,Profile
from .serializers import EmployeeSerializer
from .models import Employee, Client   # Import your Employee and Client models
from .serializers import EmployeeSerializer, ClientSerializer, ProfileSerializer, UserSerializer  # Import your serializers
from .models import User, Company, Profile
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to the API root!',
    })

class GetEmployeeListView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        employees = Employee.objects.all()
        serializer = self.serializer_class(employees, many=True)

        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched employees',
            'employees': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)    


class GetClientListView(APIView):
    serializer_class = ClientSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        clients = Client.objects.all()
        serializer = self.serializer_class(clients, many=True)

        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched clients',
            'clients': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)


class GetEmployeeView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
            serializer = self.serializer_class(employee)

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched employee',
                'employee': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:

            return Response('User not found', status= status.HTTP_404_NOT_FOUND)

       
class GetClientView(APIView):
    serializer_class = ClientSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            client = request.user
            serializer = self.serializer_class(client)

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched client',
                'client': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        except Client.DoesNotExist:

            return Response('User not found', status= status.HTTP_404_NOT_FOUND)
       
class CreateEmployeeAPIView(APIView):
    employee_serializer_class = EmployeeSerializer
    profile_serializer_class = ProfileSerializer

    permission_classes = (AllowAny,)
    
    def post(self, request, companyName):
        try:
            company_instance = Company.objects.filter(company_name = companyName).values()
            print(company_instance)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        employee_serializer = self.employee_serializer_class(data=request.data['employee'], context={'companyName': companyName})
        profile_serializer = self.profile_serializer_class(data=request.data['employee']['profile'])
       
        employee_valid = employee_serializer.is_valid(raise_exception=True)
        profile_valid = profile_serializer.is_valid(raise_exception=True)
    
        if employee_valid and profile_valid:  
            employee_instance = employee_serializer.save()
            print('employee_instance', employee_instance)
            profile_serializer.save(employee=employee_instance)
           
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'employee successfully created!',
                'employee': EmployeeSerializer(employee_instance).data,
            }
            return Response(response, status=status_code)
        return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """
    user_serializer_class = UserSerializer
    profile_serializer_class = ProfileSerializer

    permission_classes = (AllowAny,)
    
    def post(self, request):
        user_serializer = self.user_serializer_class(data=request.data['employee']['user'])
        profile_serializer = self.profile_serializer_class(data=request.data['employee']['profile'])
       
        user_valid = user_serializer.is_valid(raise_exception=True)
        profile_valid = profile_serializer.is_valid(raise_exception=True)
    
        if user_valid and profile_valid:  
            user_instance = user_serializer.save()
            print('user_instance', user_instance)
            profile_serializer.save(employee=user_instance)
           
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'employee successfully created!',
                'employee': EmployeeSerializer(user_instance).data,
            }
            return Response(response, status=status_code)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
class CreateClientAPIView(APIView):
    client_serializer_class = ClientSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request, companyName):
        try:
            company_instance = Company.objects.filter(company_name = companyName).values()
            print(company_instance)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        client_serializer = self.client_serializer_class(data=request.data['client'], context={'companyName': companyName})
        client_valid = client_serializer.is_valid(raise_exception=True)
    
        if client_valid:  
            client_instance = client_serializer.save()
            print('client_instance', client_instance)
           
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'client successfully created!',
                'client': ClientSerializer(client_instance).data,
            }
            return Response(response, status=status_code)
        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class DeleteEmployeeAPIView(APIView):
    def delete(self, request, id):
        try:
            employee = Employee.objects.get(pk=id)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DeleteClientAPIView(APIView):
    def delete(self, request, id):
        try:
            client = Client.objects.get(pk=id)
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def EmployeeUpdateByHR(request, id):
    employee = get_object_or_404(Employee, id=id)
    print(employee.user.first_name)
    if employee.role.role_name == "HR Manager" :
        modified_data = request.data
  #  modified_by = request.user
        profile_modification = ProfileModification.objects.create(
            user=employee.user,

            modified_by= employee.role,
            modified_date=timezone.now(),
            modified_data=modified_data
        )
        for field_name, field_value in request.data.items():
                if field_name == "job_title":  # Replace with the actual field name
                    setattr(employee, "job_title", field_value) 

        employee.save()
        employee.profilemodification.add(profile_modification)

        serializer = EmployeeSerializer(employee, many=False)
        return Response(serializer.data)
    return Response({"message": "You cannot update this employee"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def ClientUpdateView(request, id):
    client = get_object_or_404(Client, id=id)

    print(client.user.first_name)

    if client.user.is_superuser == True :
        return Response({"message": "You cannot update this client"}, status=status.HTTP_403_FORBIDDEN)
    modified_data = request.data
    modified_by = request.user
    profile_modification = ProfileModification.objects.create(
            user=client.user,
            #modified_by= ,
            modified_date=timezone.now(),
            modified_data=modified_data
        )
    for field_name, field_value in request.data.items():
                if field_name == "id":  
                    setattr(client, "id", field_value) 
    client.save()
    client.profilemodification.add(profile_modification)

    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)

@api_view(["GET", "PUT"])
def EmployeeProfile(request, id):
    user = request.user  # Get the authenticated user

    if request.method == "GET":
        # Retrieve the employee's profile based on the provided id
        employee_profile = get_object_or_404(Profile, id=id)
        serializer = ProfileSerializer(employee_profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        # Check if the authenticated user is the owner of the profile
        employee_profile = get_object_or_404(Profile, id=id)

        if employee_profile.user == user:
            serializer = ProfileSerializer(employee_profile, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "You cannot update this profile"}, status=status.HTTP_403_FORBIDDEN)