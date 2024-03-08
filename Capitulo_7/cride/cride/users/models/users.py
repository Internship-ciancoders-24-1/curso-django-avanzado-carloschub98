"""Modelo de usuario personalizado"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilidades
from cride.utils.models import CRideModel

class User(CRideModel, AbstractUser):
    """Modelo de usuario"""

    email = models.EmailField('email address', unique=True, error_messages={'unique':'Un usuario con este email ya existe'})
    
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="El número de teléfono debe ingresarse en el formato: +999999999. Se permiten hasta 15 dígitos"
    )
    phone_number = models.CharField(validators=[phone_regex],max_length=17, blank=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    is_client = models.BooleanField(
        'client status',default=True,
        help_text={
            'Ayudar a distinguir fácilmente a los usuarios y realizar consultas.',
            'Los clientes son el tipo principal de usuario.'
        }
    )
    
    is_verified = models.BooleanField(
        'verified',default=True,
        help_text={
            'establecido en verdadero cuando el usuario ha verificado su dirección de correo electrónico.'
        }
    )
    
    def __str__(self):
        """Retornando usuario"""
        return self.username
    
    def get_short_name(self):
        """Retornando username"""
        return self.username