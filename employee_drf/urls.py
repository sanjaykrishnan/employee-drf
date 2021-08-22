from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from employee.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('api/', include('employee.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
