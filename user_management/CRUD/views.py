
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Employee, Client  # Import your Employee and Client models
from .serializers import EmployeeSerializer, ClientSerializer  # Import your serializers
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
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