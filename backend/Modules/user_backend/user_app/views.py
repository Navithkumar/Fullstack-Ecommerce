from rest_framework.views import APIView
from response import success_response,error_response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AddressSerializer, RegisterSerializer, LoginSerializer
from django.db import transaction
from .models import Address, User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from pagination  import MyCustomPagination
from django.db.models import Q

class RegisterView(APIView):
    permission_classes = [] 
    def post(self, request):
        try:
            with transaction.atomic():
                serializer = RegisterSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    return success_response("User registered successfully", status=status.HTTP_201_CREATED)
                else:
                    return error_response("Validation failed", serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return error_response("Error while registering", str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [] 
    def post(self, request):
        try:  
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return success_response(
                    "User Login successfully",
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': {
                            'username': user.username,
                            'email': user.email,
                            'role': user.role,
                        }
                    }
                )
            else:
                return error_response("Invalid credentials", serializer.errors)

        except Exception as e:
            return error_response("Error while login", str(e))


class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
      try:
          users = User.objects.exclude(Q(id=request.user.id) | Q(is_superuser = 1))
          pagination = MyCustomPagination()
          result_data = pagination.paginate_queryset(users,request)
          serializer = RegisterSerializer(result_data,many=True)
          if serializer:
            return pagination.get_paginated_response(serializer.data)
          else:
              return success_response("No Products Found")
      except Exception as e:
          return error_response("Error while login", str(e))

class EditUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,id=id):
      try:
          with transaction.atomic():
            prevData = get_object_or_404(User,id=id)
            serializer = RegisterSerializer(prevData,data = request.data,partial=True)
            if serializer.is_valid():
              serializer.save()
              return success_response("User Updated Successfully",serializer.data)
            else:
                    return error_response("Validation failed", serializer.errors)
      except Exception as e:
          return error_response("User Updation Failed", str(e))

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        try:
          with transaction.atomic():
              data = get_object_or_404(User,id=id)
              data.delete()
              return success_response("User Deleted Successfully")
        except Exception as e:
            return error_response("User deletion Failed", str(e))
        


class UserAddressView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            with transaction.atomic():
                serializer = AddressSerializer(data=request.data)
                if serializer.is_valid():
                    address = serializer.save()
                    user = request.user
                    user.address_id = address.id
                    user.save(update_fields=["address_id"])
                    return success_response("User Address Successfully Added")
        except Exception as e:
            return error_response("User Address failed to save ", str(e))

class DeleteAddressView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        try:
          with transaction.atomic():
              data = get_object_or_404(Address,id=id)
              data.delete()
              return success_response("User Address Deleted Successfully")
        except Exception as e:
            return error_response("User Address deletion Failed", str(e))