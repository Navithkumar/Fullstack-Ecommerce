from .models import Category
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer
from .services import get_categories
from rest_framework.permissions import IsAuthenticated
from pagination  import MyCustomPagination
from response import success_response,error_response
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        print(user_id)
        serializer = CategorySerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save(user_id=user_id)
            return success_response("Category created successfully", serializer.data,status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return error_response(
                "Validation failed",  ve.detail,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return error_response("Error while creating category", str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            categories = get_categories()
            paginator = MyCustomPagination()
            paginated_categories = paginator.paginate_queryset(categories, request)
            return paginator.get_paginated_response(paginated_categories)

        except Exception as e:
            return error_response(
                "Failed to fetch categories",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,id):
        try:
            with transaction.atomic():
              data = get_object_or_404(Category,id=id)
              data.delete()
              return success_response("Category Deleted Successfully",status=status.HTTP_200_SUCCESS)
        except Exception as e:
            return error_response(
                "Failed to Delete categories",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def update(self,request,id):
        try:
          with transaction.atomic():
            prevData = get_object_or_404(Category,id=id)
            serializer = CategorySerializer(prevData,data = request.data,partial=True)
            if serializer.is_valid():
              serializer.save()
              return success_response("Category Updated Successfully",serializer.data)
            else:
              return error_response("Validation failed", serializer.errors)
        except Exception as e:
            return error_response(
                "Failed to update categories",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
