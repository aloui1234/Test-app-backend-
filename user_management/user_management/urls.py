from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('CRUD.urls')),  # Include the app's URLs under the 'api/' path
]
