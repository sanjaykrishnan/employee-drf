from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from employee.models import Employee


class EmployeeListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        employees = [Employee(**item) for item in validated_data]
        return Employee.objects.bulk_create(employees)

    def validate(self, data):
        validation_set = set()
        if len(data) > 20:
            raise serializers.ValidationError("File contains more than 20 items")
        for item in data:
            if item["code"] in validation_set:
                raise serializers.ValidationError(f"duplicated item: {item['code']}")
            else:
                validation_set.add(item["code"])

        return data


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        list_serializer_class = EmployeeListSerializer
        fields = ['id', 'code', 'name', 'department', 'date_of_birth', 'date_of_joining', 'age', 'experience']

    def validate(self, data):
        today = date.today()
        if data.get('date_of_birth') > today:
            raise serializers.ValidationError("Date of Birth cannot be after today's date.")
        if data.get('date_of_joining') > today:
            raise serializers.ValidationError("Date of Joining cannot be after today's date.")
        return data


class EmployeeBulkSerializer(serializers.Serializer):
    file = serializers.FileField()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
