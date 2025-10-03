from django.urls import path
from .views import CreateProductView,ListProductView,UpdateProductView,DeleteProductView,ListProductByUserView

urlpatterns = [
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('list-product/', ListProductView.as_view(), name='list-product'),
    path('update-product/<int:id>/', UpdateProductView.as_view(), name='update-product'),
    path('delete-product/<int:id>/', DeleteProductView.as_view(), name='delete-product'),
    path('user-product/', ListProductByUserView.as_view(), name='user-product'),
]

