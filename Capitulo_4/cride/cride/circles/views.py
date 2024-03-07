"""Vista de circulos"""

# Django
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Modelos
from cride.circles.models import Circle

# Serializador
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer

@api_view(['GET'])
def list_circles(request):
    """Listado de circulos"""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True) #many en true significado que son varios datos
    return Response(serializer.data)

@api_view(['POST'])
def create_circle(request):
    """Creacion de un circulo"""
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)