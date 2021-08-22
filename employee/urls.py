from rest_framework import routers
from django.urls import path, include

from employee.views import EmployeeViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls), name='employees'),
]
