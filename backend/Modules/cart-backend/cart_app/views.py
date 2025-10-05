from .models import Cart
from pagination import MyCustomPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from response import error_response,success_response
from rest_framework import status
from django.db import transaction
from .serializers import CartSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import requests
import os
from django.conf import settings 

class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        HOSTNAME = os.environ.get("PRODUCT_SERVICE_URL", "http://product_backend:8000")
        user_id = request.user.id
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            url = f"{HOSTNAME.rstrip('/')}/api/products/get-product/{product_id}/"
            print(url)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                product_data = response.json()
                price = product_data.get('price', 0)
            else:
                print(f"Product API error {response.status_code}: {response.text}")
                price = 0
        except requests.exceptions.RequestException as e:
            print(f"Product service unreachable: {e}")
            price = 0

        total_price = float(price) * int(quantity)
        try:
            cart_item, created = Cart.objects.update_or_create(
                user_id=user_id,
                product_id=product_id,
                defaults={'quantity': quantity, 'cart_price': total_price}
            )

            serializer = CartSerializer(cart_item)
            return success_response(
                "Cart created successfully",
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response(
                "Failed to create cart",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )