"""Serializador de usuarios"""
#Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

# Django rest
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Serializers
from cride.users.serializers.profile import ProfileModelSerializer

# Modelos
from cride.users.models import User, Profile

# Tasks
from cride.taskapp.tasks import send_confirmation_email


class UserModelSerializer(serializers.ModelSerializer):
    """Modelo de Usuario"""
    
    profile = ProfileModelSerializer(read_only=True)
    
    class Meta:
        """Clase meta"""
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
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
        send_confirmation_email.delay(user_pk=user.pk)
        return user
    
    
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
            
        