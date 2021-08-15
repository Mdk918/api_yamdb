from rest_framework import permissions

from reviews.models import User


class AuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """ Доступ на редактирование для автора, админа, модератора
        или только чтение. """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == User.ROLE_MODERATOR
                or request.user.role == User.ROLE_ADMIN)


class AdminOrReadOnly(permissions.BasePermission):
    """ Доступ на создание или редактирование только для амдина,
        всем остальным только для чтения. """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.ROLE_ADMIN)


class AdminOrSuperUser(permissions.BasePermission):
    """ Доступ на чтение/создание/редактирование только
        админу или суперпользователю. """

    def has_permission(self, request, view):
        user = request.user
        return (
            (user.is_authenticated and user.role == User.ROLE_ADMIN)
            or (user.is_authenticated and user.is_staff is True)
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (user.is_authenticated and user.role == User.ROLE_ADMIN)
            or (user.is_authenticated and user.is_staff is True)
        )


class AdminOrSuperUserOrModerator(permissions.BasePermission):
    """ Доступ только для админа, суперпользователя или
        модератора. """

    def has_permission(self, request, view):
        user = request.user
        return (
            (user.is_authenticated and user.role == User.ROLE_ADMIN)
            or (user.is_authenticated and user.is_staff is True)
            or (user.is_authenticated and user.role == User.ROLE_MODERATOR)
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (user.is_authenticated and user.role == User.ROLE_ADMIN)
            or (user.is_authenticated and user.is_staff is True)
            or (user.is_authenticated and user.role == User.ROLE_MODERATOR)
        )


class AdminOrAuthUser(permissions.BasePermission):
    """ Доступ к объекту для админа либи любого авторизованного
        пользователя. """

    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
            (user.is_authenticated and user.role == User.ROLE_ADMIN)
            or (user.is_authenticated and user.is_staff is True)
            or user.is_authenticated
        )
