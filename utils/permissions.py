from ninja_extra.permissions import BasePermission, IsAuthenticated


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "COMPANY"
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == "COMPANY"
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "ADMIN"
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.user_type == "ADMIN"


class IsAuthenticatedAndNotDeleted(BasePermission):
    message = "Your account is deleted\nYou can restore it by contacting us"
    def has_permission(self, request, controller) -> bool:
        return request.user.is_authenticated and not getattr(request.user, "is_deleted", False)
