from django.urls import reverse, resolve
from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from rest_framework import status

from ..views import (
    api_root,
    GetEmployeeListView,
    GetClientListView,
    GetEmployeeView,
    GetClientView,
)

class ApiViewTests(APITestCase):

    def test_api_root_view(self):
        url = reverse('api-root')
        self.assertEquals(resolve(url).func, api_root)
        
    def test_get_employee_list_view(self):
        # Assuming 'company_name' is the parameter for this URL pattern
        url = reverse('employee-list', kwargs={'company': 'company_name'})
        self.assertEquals(resolve(url).func.view_class, GetEmployeeListView)
        
    def test_get_client_list_view(self):
        # Assuming 'company_name' is the parameter for this URL pattern
        url = reverse('client-list', kwargs={'company': 'company_name'})
        self.assertEquals(resolve(url).func.view_class, GetClientListView)
        
    def test_get_employee_view(self):
        # Assuming '1' is the ID parameter for this URL pattern
        url = reverse('get-employee', kwargs={'id': 1})
        self.assertEquals(resolve(url).func.view_class, GetEmployeeView)
        
    def test_get_client_view(self):
        # Assuming '1' is the ID parameter for this URL pattern
        url = reverse('get-client', kwargs={'id': 1})
        self.assertEquals(resolve(url).func.view_class, GetClientView)

   
