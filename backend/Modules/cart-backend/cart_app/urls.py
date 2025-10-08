from django.urls import path
from .views import CartApiView

urlpatterns = [
    path('cart-api/', CartApiView.as_view(), name='cart-api'),
    path('cart-api/', CartApiView.as_view(), name='cart-api'),
]

