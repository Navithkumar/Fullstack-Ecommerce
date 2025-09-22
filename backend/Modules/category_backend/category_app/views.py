from rest_framework.views import APIView
from rest_framework import status
from .serializers import CategorySerializer
from .services import get_categories
from rest_framework.permissions import IsAuthenticated
from pagination  import MyCustomPagination
from response import success_response,error_response
from django.db import transaction
from rest_framework.exceptions import ValidationError

class CategoryCreateAPIView(APIView):
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

# class CategoryListView(APIView):
    