
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProfileSerializer  # Import your serializer

from django.shortcuts import get_object_or_404, render
from .models import Employee, ProfileModification, Profile, Client, User, Company
from .serializers import EmployeeSerializer, ClientSerializer, ProfileSerializer, CompanySerializer  # Import your serializers
from django.utils import timezone
import random
import string

from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny


@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Welcome to the API root!',
    })


class GetEmployeeListView(APIView):
    employee_serializer_class = EmployeeSerializer # helper class (employee) to generate text representation of the model
    profile_serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)

    def get(self, request, company):
        """
        Get list of employees by <company_name>
        """
        try:
            data=[]
            company = Company.objects.get(company_name=company)
            employees = Employee.objects.filter(company=company)
            
            for employee in employees:
                profile = Profile.objects.get(employee=employee)
                employee_serializer = self.employee_serializer_class(employee)
                profile_serializer = self.profile_serializer_class(profile)
                data.append({**employee_serializer.data, **profile_serializer.data}) 
          
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched employees',
                'employees': data # show data here
            }
            return Response(response, status=status.HTTP_200_OK)   
        except Company.DoesNotExist:
            return Response("Company not found", status= status.HTTP_404_NOT_FOUND) # if company is not found, show error 404


class GetClientListView(APIView):
    client_serializer_class = ClientSerializer  # Helper class to generate text representation of the model
    company_serializer_class = CompanySerializer 
    permission_classes = (AllowAny,)  # Anyone can consume the API (no login/pass)

    def get(self, request, company):
        """
        Get list of clients by <company_name>
        """
        try:
            company = Company.objects.get(company_name=company) # get companies with that name
            company_serializer = self.company_serializer_class(company) # convert company to text representation

           
            clients_ids = company_serializer.data['clients'] # get the ids of the clients [1,2,3,4...]
            clients = Client.objects.filter(id__in=clients_ids) # get clients with these ids
            clients_serializer = self.client_serializer_class(clients, many=True) # convert the result to text representation
          
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': f'Successfully fetched clients for {company}',
                'clients': clients_serializer.data  # Show data in the JSON response
            }

            return Response(response, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response("Company not found", status=status.HTTP_404_NOT_FOUND)  # If company is not found, show error 404


class GetEmployeeView(APIView):
    employee_serializer_class = EmployeeSerializer
    profile_serializer_class = ProfileSerializer
    permission_classes = (AllowAny,) # anyone can consume the api (no login/pass)

    def get(self, request, id):
        """
        Get employee by <id>
        """
        try:
            employee = Employee.objects.get(id=id) # get employees with that "id"
            profile = Profile.objects.get(employee=employee)
            
            employee_serializer = self.employee_serializer_class(employee)  # convert to text representation
            profile_serializer = self.profile_serializer_class(profile)
            
            data = {**employee_serializer.data, **profile_serializer.data}

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched employee',
                'employee': data
            }

            return Response(response, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            response = {
                'success': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Employee not found'
            }
            return Response(response, status= status.HTTP_404_NOT_FOUND)

       
class GetClientView(APIView):
    serializer_class = ClientSerializer
    permission_classes = (AllowAny,)

    def get(self, request, id):
        """
        Get client by <id>
        """
        try:
            client = Client.objects.get(id=id) # get client with that "id"
            serializer = self.serializer_class(client) # convert to text representation

            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched client',
                'client': serializer.data
            }

            return Response(response, status=status.HTTP_200_OK)
        except Client.DoesNotExist:
            response = {
                            'success': False,
                            'status_code': status.HTTP_404_NOT_FOUND,
                            'message': 'Client not found'
            }
            return Response(response, status= status.HTTP_404_NOT_FOUND)
        

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
        
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        request.data['employee']['user']['password'] = password

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
        
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        request.data['client']['user']['password'] = password

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
            # Delete the Employee object
            employee = Employee.objects.get(pk=id)
            employee.delete()

            # Now update the User object with the same ID
            try:
                user = User.objects.get(pk=id)
                user.is_deleted = True  # Set is_deleted to True
                user.is_active = False  # Set is_active to False
                user.save()
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteClientAPIView(APIView):
    def delete(self, request, id):
        try:
            # Delete the Client object
            client = Client.objects.get(pk=id)
            client.delete()

            # Now update the User object with the same ID
            try:
                user = User.objects.get(pk=id)
                user.is_deleted = True  # Set is_deleted to True
                user.is_active = False  # Set is_active to False
                user.save()
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def SimpleEmployeeUpdate(request, id):
    employee = get_object_or_404(Employee, id=id)
    profile = get_object_or_404(Profile, employee=employee)
    
    for field_name, field_value in request.data.items():
        if hasattr(profile, field_name):
            setattr(profile, field_name, field_value)

    profile.save()

    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def SimpleClientUpdate(request, id):
    client = get_object_or_404(Client, id=id)
    
    for field_name, field_value in request.data.items():
        if hasattr(client, field_name):
            setattr(client, field_name, field_value)

    client.save()

    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def EmployeeUpdateByHR(request, id):
    employee = get_object_or_404(Employee, id=id)

    if employee.role.role_name == "HR Manager" :
        modified_data = request.data
  #  modified_by = request.user
        profile_modification = ProfileModification.objects.create(
            user=employee.user,

            modified_by= employee.role,
            modified_date=timezone.now(),
            modified_data=modified_data
        )
        for field_name, field_value in modified_data.items():
            if hasattr(employee, field_name):
                setattr(employee, field_name, field_value)

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
    for field_name, field_value in modified_data.items():
            if hasattr(client, field_name):
                setattr(client, field_name, field_value)
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