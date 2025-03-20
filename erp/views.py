from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # This will call the create() method in the serializer
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_user(request): 
    users = User.objects.all()
    serializer = UserRegistrationSerializer(users, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, email):  # Add the `email` parameter
    try:
        user = User.objects.get(email=email)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
