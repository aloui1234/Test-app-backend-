
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer  # Import your serializer

from django.shortcuts import get_object_or_404, render
from .models import Employee, ProfileModification,Profile
from .serializers import EmployeeSerializer
from .models import Employee, Client  # Import your Employee and Client models
from .serializers import EmployeeSerializer, ClientSerializer  # Import your serializers
from .models import User
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