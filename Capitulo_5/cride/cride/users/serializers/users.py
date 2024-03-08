"""Serializador de usuarios"""
#Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django rest
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Modelos
from cride.users.models import (User, Profile)

# Utilities
import jwt
from datetime import timedelta

class UserModelSerializer(serializers.ModelSerializer):
    """Modelo de Usuario"""
    class Meta:
        """Clase meta"""
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserLoginSerializer(serializers.Serializer):
    """Serializador de login de usuario"""
    email = serializers.EmailField()
    password=serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        """Verificando las credenciales"""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credenciales incorrectas')
        if not user.is_verified:
            raise serializers.ValidationError('Tu cuenta no ha sido activado :(')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """Generar o recuperar un nuevo toke"""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
        

class UserSignUpSerializer(serializers.Serializer):
    """Registro de usuario"""
    
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="El número de teléfono debe ingresarse en el formato: +999999999. Se permiten hasta 15 dígitos"
    )
    phone_number = serializers.CharField(validators=[phone_regex])
    
    # password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    
    # Names
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    
    def validate(self, data):
        """Coincidencia de password"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        
        if passwd != passwd_conf:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        password_validation.validate_password(passwd)
        return data
    
    def create(self, data):
        """Validacion para usuario y perfil"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user
    
    def send_confirmation_email(self,user):
        """Metodo de configuracion de email"""
        
        verification_token=self.gen_verification_token(user)
        subject = 'Welcome @{}! Verificando tu cuenta para empezar a usar Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token':verification_token, 'user':user}
        )        
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
        
    def gen_verification_token(self, user):
        """Crear JWT Token para que el usuario pueda verificar su cuenta"""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user':user.username,
            'exp': int(exp_date.timestamp()),
            'type':'email_confirmation'
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
    
class AccountVerificationSerializer(serializers.Serializer):
    """Serializador de verificacion de usuario"""
    
    token = serializers.CharField()
    
    def validate_token(self, data):
        """Validando el token"""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('El link de verificacion ha caducado.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token invalido!')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Token invalido')
        self.context['payload'] = payload
        return data

    def save(self):
        """Actualizar el campo de verficacion de usuario."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
            
        