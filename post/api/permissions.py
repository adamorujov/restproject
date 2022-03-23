from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
        
    message = "You must be the owner of this post."
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser