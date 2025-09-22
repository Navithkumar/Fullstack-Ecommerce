from django.urls import path
from .views import CategoryCreateAPIView

urlpatterns = [
    path('create-category/', CategoryCreateAPIView.as_view(), name='register'),
]