"""App de usuario"""

# Django
from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    """Configuracion de app usuario"""
    
    name = 'cride.users' #modulo en el que esta mas la app
    verbose_name = 'Users'