from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from response import error_response,success_response
from rest_framework import status
from django.db import transaction
from .serializers import ProductsSerializer
from rest_framework.exceptions import ValidationError

class CreateProductView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    user = request.user.id
    serializer = ProductsSerializer(data=request.data)
    try:
      serializer.is_valid(raise_exception=True)
      with transaction.atomic():
        serializer.save(user_id=user)
        return success_response("Product created successfully", serializer.data,status=status.HTTP_201_CREATED)

    except ValidationError as ve:
            return error_response(
                "Validation failed",  ve.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
      return error_response("Error creating product",str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
