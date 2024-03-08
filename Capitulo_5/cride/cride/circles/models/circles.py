"""Modelo de circulo"""

# Django
from django.db import models

# Utilidades
from cride.utils.models import CRideModel

class Circle(CRideModel):
    """Modelo de circulo"""
    
    """Para unirse a un circulo debe ser mediante una invitacion"""
    
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)
    
    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
    
    members = models.ManyToManyField(
        'users.User',
        through='circles.Membership',
        through_fields=('circle', 'user')
    )
    
    # Estadisticas
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)
    
    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Los círculos verificados también se conocen como comunidades oficiales.'
    )
    
    is_public = models.BooleanField(
        default=True,
        help_text='Los círculos públicos se enumeran en la página principal para que todos sepan sobre su existencia.'
    )
    
    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Los círculos limitados pueden crecer hasta un número fijo de miembros.'
    )
    
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='Si el círculo es limitado, este será el límite de número de miembros.'
    )
    
    def __str__(self):
        """Retornando al momento de instanciar"""
        return self.name
    
    class Meta(CRideModel.Meta):
        """Meta class"""
        
        ordering = ['-rides_taken', '-rides_offered']