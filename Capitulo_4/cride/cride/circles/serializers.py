"""Serializador de circulos"""

# Django
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Modelos
from cride.circles.models import Circle

class CircleSerializer(serializers.Serializer):
    """Serilizador de circulos"""
    
    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()
    
class CreateCircleSerializer(serializers.Serializer):
    """Serializador de datos de entrada"""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.CharField(max_length=40, validators=[UniqueValidator(queryset=Circle.objects.all())])
    about = serializers.CharField(max_length=155, required=False)
    
    def create(self,data):
        """Modificando el metodo create"""
        return Circle.objects.create(**data)