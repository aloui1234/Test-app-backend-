
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('employees/', views.GetEmployeeListView.as_view(), name='employee-list'),
    path('clients/', views.GetClientListView.as_view(), name='client-list'),
     # Add URL patterns for GetEmployeeView and GetClientView
    path('get-employee/', views.GetEmployeeView.as_view(), name='get-employee'),
    path('get-client/', views.GetClientView.as_view(), name='get-client'),
    
    path('employees/<int:id>/', views.EmployeeUpdateByHR, name='employee-update'),
    path('clients/<int:id>/', views.ClientUpdateView, name='client-update'),
    path('employees/<int:id>/profile/', views.EmployeeUpdateBySelf, name='employee-update'),
    
    path('create-employee/<str:companyName>', views.CreateEmployeeAPIView.as_view(), name='create_employee'),
    path('delete-employee/<int:id>', views.DeleteEmployeeAPIView.as_view(), name='delete_employee'),
    path('create-client/<str:companyName>', views.CreateClientAPIView.as_view(), name='create_client'),
    path('delete-client/<int:id>', views.DeleteClientAPIView.as_view(), name='delete_client')
    ]
