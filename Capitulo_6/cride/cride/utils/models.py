"""Modelo de utilidades de django"""

from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base model
        Es una clase abstracta, esto significa que no se vera reflejado en la bd
    """
    
    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Fecha y hora en la que se creo el objeto'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Fecha y hora en la que el objeto fue modificado por última vez'
    )
    
    class Meta:
        """Opcion de meta"""
        abstract = True
        
        get_latest_by = 'created'
        ordering = ['-created']
