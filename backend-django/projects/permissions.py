from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminForDelete(BasePermission):
    """
    Read: allowed to everyone
    Delete: allowed only to project owner or staff/admin
    Update: allowed only to project owner or staff/admin
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return obj.creator == request.user or request.user.is_staff