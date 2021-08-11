from rest_framework import permissions


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin')


class AdminOrReadOnly(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin')


class AdminOrSuperUser(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_permission(self, request, view):
        return ((request.user.is_authenticated and request.user.role == 'admin')
                or (request.user.is_authenticated and
                    request.user.is_staff is True))

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated and request.user.role == 'admin')
                or (request.user.is_authenticated and
                    request.user.is_staff is True))


class AdminOrAuthUser(permissions.BasePermission):
    """ Создаем и настраиваем пермишены для сериализаторов """

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated and request.user.role == 'admin')
                or (request.user.is_authenticated and
                    request.user.is_staff is True) or
                request.user.is_authenticated)
