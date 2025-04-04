from erp.serializers import EmployeeRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from erp.models import Employees

# employee registration
@api_view(['POST'])
def register_employee(request):
    serializer = EmployeeRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  
        return Response({"message": "Employee created successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_employees(request): 
    users = Employees.objects.all()
    serializer = EmployeeRegistrationSerializer(users, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
