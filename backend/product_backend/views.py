from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

# Create your views here.


class CreateProductView(APIview):
  permission_classes = [IsAuthenticated]

  def post(self,request):
    try:

    

    except as Exception:
      