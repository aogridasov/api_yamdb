from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsPost(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_moderator
