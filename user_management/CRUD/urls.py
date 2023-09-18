
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('employees/<str:company>', views.GetEmployeeListView.as_view(), name='employee-list'), # <company> is the name of the company
    path('clients/<str:company>', views.GetClientListView.as_view(), name='client-list'),
    path('get-employee/<int:id>/', views.GetEmployeeView.as_view(), name='get-employee'), # <id> is the id of employee
    path('get-client/<int:id>/', views.GetClientView.as_view(), name='get-client'), # <id> is the id of client
    
    path('update-employee/<int:id>/', views.SimpleEmployeeUpdate, name='employee-update'),
    path('update-client/<int:id>/', views.SimpleClientUpdate, name='client-update'),

    #path('update-employee-hr/<int:id>/', views.EmployeeUpdateByHR, name='employee-hr-update'),
    #path('update-client/<int:id>/', views.ClientUpdateView, name='client-update'),
    #path('update-employee-profile/<int:id>', views.EmployeeProfile, name='employee-profile-update'),
    
    path('create-employee/<str:companyName>', views.CreateEmployeeAPIView.as_view(), name='create_employee'),
    path('delete-employee/<int:id>', views.DeleteEmployeeAPIView.as_view(), name='delete_employee'),
    path('create-client/<str:companyName>', views.CreateClientAPIView.as_view(), name='create_client'),
    path('delete-client/<int:id>', views.DeleteClientAPIView.as_view(), name='delete_client')
    ]
