from django.urls import path
from .views import RegisterView, LoginView,ListUsersView,EditUsersView,DeleteUserView,UserAddressView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('list-users/', ListUsersView.as_view(), name='list-users'),
    path('edit-users/<int:id>', EditUsersView.as_view(), name='edit-users'),
    path('delete-users/<int:id>', DeleteUserView.as_view(), name='delete-users'),
    path('add-address/', UserAddressView.as_view(), name='address'),
]
