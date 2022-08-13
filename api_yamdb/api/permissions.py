from rest_framework import permissions


<<<<<<< HEAD
class IsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого контента запрещено!'
=======
class IsAllowedToEditOrReadOnly(permissions.BasePermission):
>>>>>>> 0340f64 (commit before pulling from updated master)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
