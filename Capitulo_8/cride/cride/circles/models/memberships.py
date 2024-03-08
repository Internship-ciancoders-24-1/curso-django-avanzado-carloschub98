"""Modelo de membership."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Membership(CRideModel):
    """
    Modelo de membresía.
    Una membresía es la tabla que mantiene la relación entre
    un usuario y un círculo.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text="Los administradores del círculo pueden actualizar los datos del círculo y administrar a sus miembros."
    )

    # Invitaciones
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by' #Esto es para identificar la segunda llamada al modelo de usuario,asi lo dice django
    )

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Sólo los usuarios activos pueden interactuar en el círculo.'
    )

    def __str__(self):
        """Retornando username y su circulo o grupo."""
        return '@{} at #{}'.format(
            self.user.username,
            self.circle.slug_name
        )