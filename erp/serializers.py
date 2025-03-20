from rest_framework import serializers
from django.contrib.auth import get_user_model
from ZCHPC_ERP.erp_project.erp.models import Employee

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'firstname', 'surname', 'role', 'employeeid', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_employeeid(self, value):
        """Ensure employee ID is unique."""
        if User.objects.filter(employeeid=value).exists():
            raise serializers.ValidationError("This Employee ID is already in use.")
        return value

    def create(self, validated_data):
        """Create a new user with a default password."""
        # Use email as the username
        validated_data['username'] = validated_data['email']
        
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Password will be hashed automatically
            firstname=validated_data.get('firstname', ''),
            surname=validated_data.get('surname', ''),
            role=validated_data.get('role', ''),
            employeeid=validated_data.get('employeeid', '')
        )
        return user
    
    def create_employee(self, validated_data):
        """Create a new user with a default password."""
        # Use email as the username
        validated_data['username'] = validated_data['email']
        
        # Create the user
        user = Employee.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Password will be hashed automatically
            firstname=validated_data.get('firstname', ''),
            surname=validated_data.get('surname', ''),
            department=validated_data.get('department', ''),
            employeeid=validated_data.get('employeeid', ''),
            contractFrom=validated_data.get('contractFrom', ''),
            contractTo=validated_data.get('contractTo', ''),
        )
        return user