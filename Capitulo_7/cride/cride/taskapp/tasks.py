"""Tareas de celery"""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Models
from cride.users.models import User

# Celery
from celery.decorators import task, periodic_task
from cride.rides.models import Ride

# Utilities
import jwt
import time 
from datetime import timedelta

def gen_verification_token(user):
    """Crear JWT Token para que el usuario pueda verificar su cuenta"""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user':user.username,
        'exp': int(exp_date.timestamp()),
        'type':'email_confirmation'
    }
        
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
        """Metodo de configuracion de email"""
        # for i in range(10):
        #     time.sleep(1)
        #     print("sleeping", str(i+1))
        user = User.objects.get(pk=user_pk)
        verification_token=gen_verification_token(user)
        subject = 'Welcome @{}! Verificando tu cuenta para empezar a usar Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token':verification_token, 'user':user}
        )        
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
        
@periodic_task(name='disable_finished_rides', run_every=timedelta(seconds=5))
def disable_finished_rides():
    """Deshabilitar la finalizacion de viaje."""
    now = timezone.now()
    offset = now + timedelta(seconds=5)

    # Update rides that have already finished
    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=False)