from functools import partial
from .models import Products
from pagination import MyCustomPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from response import error_response,success_response
from rest_framework import status
from django.db import transaction
from .serializers import ProductsSerializer
from rest_framework.exceptions import ValidationError
from .services import get_products
from django.shortcuts import get_object_or_404

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

class ListProductView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request):
    try:
      products = get_products()
      pagination = MyCustomPagination()
      data = pagination.paginate_queryset(products, request)
      return pagination.get_paginated_response(data)

    except Exception as e:
      return error_response("Error Fetching product",str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self,request,id):
      try:
        product = get_object_or_404(Products, id=id)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Product Update successfully", serializer.data,status=status.HTTP_201_CREATED)
      except Exception as e:
        return error_response("Error Updating product",str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProductView(APIView):
  permission_classes = [IsAuthenticated]

  def delete(self,request,id):
      try:
        product = get_object_or_404(Products, id=id)
        product.delete()
        return success_response("Product Deleted successfully",status=status.HTTP_201_CREATED)
      except Exception as e:
        return error_response("Error Deleting product",str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)