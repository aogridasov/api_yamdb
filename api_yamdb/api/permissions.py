from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsPost(BasePermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class HasRightsOrReadOnly(BasePermission):
    message = 'Вы не авторизованы на данный запрос, sorry buddy'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (
                        obj.author == request.user
                        or request.user.is_moderator
                        or request.user.is_admin
                    )
                    )
                )
