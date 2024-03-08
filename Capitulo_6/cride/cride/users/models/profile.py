"""Modelo de perfil"""

# Django
from django.db import models

# utilidades
from cride.utils.models import CRideModel

class Profile(CRideModel):
    """Modelo de perfil de usuario"""
    
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    
    biography = models.TextField(max_length=500, blank=True)
    
    # Estadisticas
    rides_taken=models.PositiveIntegerField(default=0)
    rides_offered=models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=5.0,
        help_text='Reputación del usuario basada en los viajes realizados y ofrecidos.'
    )
    
    def __str__(self):
        """Retornando la representacion del usuario"""
        return str(self.user)