"""Serializador de circulos"""

# Django REST Framework
from rest_framework import serializers

# Modelo
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo circulo."""
    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=377
    )
    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""

        model = Circle
        fields = (
            'id','name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken',
        )

    def validate(self, data):
        """Asegúrese de que tanto Members_limit como is_limited estén presentes."""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('Si el círculo es limitado, se debe proporcionar un límite de miembros.')
        return data