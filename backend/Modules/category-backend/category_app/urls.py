from django.urls import path
from .views import CategoryCreateView,CategoryListView

urlpatterns = [
    path('create-category/', CategoryCreateView.as_view(), name='create-category'),
    path('get-category/', CategoryListView.as_view(), name='get-category'),
]