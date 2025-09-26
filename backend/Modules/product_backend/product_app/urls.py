from django.urls import path
from .views import CreateProductView,ListProductView

urlpatterns = [
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('list-product/', ListProductView.as_view(), name='list-product'),
]

