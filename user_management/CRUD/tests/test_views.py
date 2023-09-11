#from django.urls import reverse
#from rest_framework.test import APITestCase
#from rest_framework import status
#from .models import Employee, Client, Company

#class GetEmployeeListViewTest(APITestCase):
    #def test_get_employee_list_by_company(self):
        # Create a company
        #company = Company.objects.create(company_name="Test Company")

        # Create employees for the company
        #employee1 = Employee.objects.create(name="Employee 1", company=company)
        #employee2 = Employee.objects.create(name="Employee 2", company=company)

        #url = reverse('get-employee-list', args=[company.company_name])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(len(response.data['employees']), 2)

    #def test_get_employee_list_by_nonexistent_company(self):
        # Attempt to get employees for a nonexistent company
        #url = reverse('get-employee-list', args=['NonexistentCompany'])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#class GetClientListViewTest(APITestCase):
    #def test_get_client_list_by_company(self):
        # Create a company
        #company = Company.objects.create(company_name="Test Company")

        # Create clients for the company
        #client1 = Client.objects.create(name="Client 1", company=company)
        #client2 = Client.objects.create(name="Client 2", company=company)

        #url = reverse('get-client-list', args=[company.company_name])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(len(response.data['clients']), 2)

    #def test_get_client_list_by_nonexistent_company(self):
        # Attempt to get clients for a nonexistent company
        #url = reverse('get-client-list', args=['NonexistentCompany'])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#lass GetEmployeeViewTest(APITestCase):
    #def test_get_employee_by_id(self):
        # Create an employee
        #employee = Employee.objects.create(name="Employee 1")

        #url = reverse('get-employee', args=[employee.id])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data['employee']['name'], "Employee 1")

    #def test_get_nonexistent_employee(self):
        # Attempt to get a nonexistent employee
        #url = reverse('get-employee', args=[999])  # Assuming 999 is a nonexistent ID
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#class GetClientViewTest(APITestCase):
    #def test_get_client_by_id(self):
        # Create a client
        #client = Client.objects.create(name="Client 1")

        #url = reverse('get-client', args=[client.id])
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data['client']['name'], "Client 1")

    #def test_get_nonexistent_client(self):
        # Attempt to get a nonexistent client
        #url = reverse('get-client', args=[999])  # Assuming 999 is a nonexistent ID
        #response = self.client.get(url)

        #self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
