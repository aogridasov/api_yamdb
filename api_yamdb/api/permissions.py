from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_admin
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


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user.is_authenticated and request.user.is_admin
        )
