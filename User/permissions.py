from rest_framework import permissions


class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == 1)


class IsPerson(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == 2)
