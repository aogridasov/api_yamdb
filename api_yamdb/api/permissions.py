from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsPost(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_moderator
