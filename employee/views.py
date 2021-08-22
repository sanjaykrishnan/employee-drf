import csv

from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from employee.models import Employee
from employee.serializers import EmployeeSerializer, EmployeeBulkSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='bulk-save', permission_classes=[permissions.IsAdminUser])
    def bulk_save(self, request):
        serializer = EmployeeBulkSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']

            if not file_obj.name.endswith('.csv'):
                return Response({'error': 'Please upload a file with csv extension.'},
                                status=status.HTTP_400_BAD_REQUEST)

            with open(str(file_obj)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                data = []
                for index, row in enumerate(csv_reader):
                    if len(row) > 5:
                        return Response({'error': 'Columns cannot be more than 5.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if index != 0:
                        data.append({'code': row[0], 'name': row[1], 'department': row[2], 'date_of_birth': row[3],
                                     'date_of_joining': row[4]})

            data_list = EmployeeSerializer(data=data, many=True, allow_empty=False)
            if data_list.is_valid():
                data_list.save()
                return Response({'success': 'saved records.'})
            else:
                return Response(data_list.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
