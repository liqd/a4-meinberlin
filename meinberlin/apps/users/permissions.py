from rest_framework import permissions

from adhocracy4.projects.guest_users import is_guest_user


class IsRegularUser(permissions.BasePermission):
    """Allow only authenticated, non-guest users.

    Use for API viewsets that gate via ``permission_classes`` (e.g. the
    notification APIs) rather than django-rules. ``is_guest_user`` returns
    ``False`` when django-guest-user is not installed, so this degrades to
    ``IsAuthenticated``.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated) and not is_guest_user(user)
