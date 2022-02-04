from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Create/delete allowed to admins. Safe methods allowed to everyone."""
    message = 'Недостаточно прав доступа'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Edit/delete allowed to admins/moderators/authors.
    Safe methods allowed to everyone.
    """
    message = 'Недостаточно прав доступа'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator')
