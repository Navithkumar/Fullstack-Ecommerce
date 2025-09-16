from django.urls import path
from .views import CreateProductView

urlpatterns = [
    path('create-products/', CreateProductView.as_view(), name='create-products'),
]
