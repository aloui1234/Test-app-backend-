
from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('employees/', views.GetEmployeeListView.as_view(), name='employee-list'),
    path('clients/', views.GetClientListView.as_view(), name='client-list'),
     # Add URL patterns for GetEmployeeView and GetClientView
    path('get-employee/', views.GetEmployeeView.as_view(), name='get-employee'),
    path('get-client/', views.GetClientView.as_view(), name='get-client'),
    ]