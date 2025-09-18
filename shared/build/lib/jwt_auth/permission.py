from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == 1

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == 2

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == 3
