from django.urls import path
from .views import CartApiView

urlpatterns = [
    path('cart-api/', CartApiView.as_view(), name='cart-create'),
    path('cart-api/', CartApiView.as_view(), name='cart-api-get'),
    path('cart-api/<int:cart_id>/product/<int:product_id>/', CartApiView.as_view(), name='cart-api-delete'),
]

