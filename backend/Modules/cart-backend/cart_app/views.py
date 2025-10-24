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
from .services import get_cart_items,clear_cache


class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        HOSTNAME = os.environ.get("PRODUCT_SERVICE_URL", "http://product-backend:8000")
        user_id = request.user.id
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            url = f"{HOSTNAME.rstrip('/')}/get-product/{product_id}/"
            headers = {"Authorization": request.headers.get("Authorization")}
            response = requests.get(url, headers=headers,timeout=5)
            if response.status_code == 200:
                product_data = response.json()
                price = float(product_data.get('data', {}).get('product_price', 0))
            else:
                print(f"Product API error {response.status_code}: {response.text}")
                price = 0
        except requests.exceptions.RequestException as e:
            print(f"Product service unreachable: {e}")
            price = 0

        total_price = float(price) * int(quantity)
        try:
            cart_item = Cart.objects.filter(user_id=user_id, product_id=product_id).first()

            if cart_item:
                new_quantity = cart_item.quantity + quantity
                total_price = price * new_quantity
                cart_item.quantity = new_quantity
                cart_item.cart_price = total_price
                cart_item.save()
                created = False
            else:
                total_price = price * quantity
                cart_item = Cart.objects.create(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    cart_price=total_price
                )
                created = True
            
            clear_cache(user_id)

            serializer = CartSerializer(cart_item)
            message = "Cart created successfully" if created else "Cart updated successfully"
            return success_response(message, serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(
                "Failed to create cart",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
          
    def get(self,request):
        try:
          user_id = request.user.id
          data = get_cart_items(user_id)
          pagination = MyCustomPagination()
          data = pagination.paginate_queryset(data, request)
          return pagination.get_paginated_response(data)
        except Exception as e:
            return error_response(
                "Failed to get cart",
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, cart_id, product_id):
      try:
          with transaction.atomic():
              cart_item = get_object_or_404(Cart, cart_id=cart_id, product_id=product_id)
              cart_item.delete()

              return success_response(
                  "Product removed from cart successfully",
                  status=status.HTTP_200_OK
              )

      except Exception as e:
          return error_response(
              "Failed to remove product from cart",
              str(e),
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )