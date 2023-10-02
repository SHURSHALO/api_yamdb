from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


class AuthorOrReadOnly(permissions.BasePermission):
    '''Кастомное разрешение, разрешает доступ только автору объекта.'''

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    '''Кастомное разрешение, только для чтения для безопасных методов.'''
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ModeratorOrAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Здесь предполагается, что у пользователя есть атрибут 'is_moderator',
        # который показывает его роль в системе. Вы можете адаптировать это под
        # свою систему ролей или аутентификации.
        return request.user.is_authenticated or request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь автором объекта или модератором.
        return obj.author == request.user or request.user.is_moderator


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.is_admin


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    """Доступ только для администратора, модератора и автора объекта."""

    def has_permission(self, request, view):
        if (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        ):
            return True
        raise AuthenticationFailed("Требуется авторизация")

    def has_object_permission(self, request, view, obj):
        if (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        ):
            return (
                    request.method in permissions.SAFE_METHODS
                    or request.user.role in ["admin", "moderator"]
                    or request.user.is_superuser
                    or obj.author == request.user
            )
        raise AuthenticationFailed("Требуется авторизация")


class ReadOnly(permissions.BasePermission):
    """Только чтение."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserOrAdmin(permissions.BasePermission):
    """Доступ только для суперпользователи или администратора."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_admin)
