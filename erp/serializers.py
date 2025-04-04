from rest_framework import serializers
from .models import CustomUser, Employees

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'employeeid', 'firstname', 'isActive', 'surname', 'role', 'department', 'password', 'salary', 'contractFrom', 'contractTo']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            firstname=validated_data.get('firstname', ''),
            surname=validated_data.get('surname', ''),
            role=validated_data.get('role', ''),
            department=validated_data.get('department', ''),
            salary=validated_data.get('salary', None),
            contractFrom=validated_data.get('contractFrom', None),
            contractTo=validated_data.get('contractTo', None),
        )
        return user
    
class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['email', 'employeeid', 'firstname', 'isActive', 'surname', 'position', 'department',  'usd_salary', 'zig_salary', 'contractFrom', 'contractTo', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if Employees.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = Employees.objects.create(
            email=validated_data['email'],
            firstname=validated_data.get('firstname', ''),
            surname=validated_data.get('surname', ''),
            position=validated_data.get('position', ''),
            department=validated_data.get('department', ''),
            phone = validated_data.get('phone', ''),
            usd_salary=validated_data.get('usd_salary', None),
            zig_salary=validated_data.get('zig_salary', None),
            contractFrom=validated_data.get('contractFrom', None),
            contractTo=validated_data.get('contractTo', None),
        )
        return user
    
class EmployeePayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['employeeid', 'firstname', 'isActive', 'surname', 'position', 'department',  'contractFrom', 'contractTo', 'phone', 'usd_salary', 'zig_salary']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if Employees.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = Employees.objects.create(
            email=validated_data['email'],
            firstname=validated_data.get('firstname', ''),
            surname=validated_data.get('surname', ''),
            position=validated_data.get('position', ''),
            department=validated_data.get('department', ''),
            phone = validated_data.get('phone', ''),
            usd_salary=validated_data.get('usd_salary', None),
            zig_salary=validated_data.get('zig_salary', None),
            contractFrom=validated_data.get('contractFrom', None),
            contractTo=validated_data.get('contractTo', None),
        )
        return user
