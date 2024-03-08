"""Permisos para la clase de circulos"""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Permitir el acceso solo a los administradores del círculo."""

    def has_object_permission(self, request, view, obj):
        """Verifique que el usuario sea miembro del obj."""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True