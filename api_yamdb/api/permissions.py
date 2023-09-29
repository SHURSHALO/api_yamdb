from rest_framework import permissions


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
        return request.user and (
            request.user.is_superuser or request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_admin
