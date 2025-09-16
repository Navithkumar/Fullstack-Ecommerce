from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from response import error_response,success_response
from rest_framework import status
from .serializers import ProductsSerializer

class CreateProductView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    try:
      with transaction.atomic():
        serilizer = ProductsSerializer(data = request.data)
        if serilizer.is_valid():
          serilizer.save()
          return success_response('Product Created Successfully',status=status.HTTP_201_CREATED)
    except Exception as e:
      return error_response('Product Creation Failed', str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)