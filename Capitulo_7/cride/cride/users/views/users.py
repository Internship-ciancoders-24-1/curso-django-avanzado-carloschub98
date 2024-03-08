"""Vista de usuarios"""

# Django Rest
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

# Serilizador
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Conjunto de vistas de usuario.
    Gestionar el registro, el inicio de sesión y la verificación de la cuenta.
    """
    # queryset = User.objects.filter(is_active=True, is_client=True)
    # serializer_class = UserModelSerializer
    # lookup_field = 'username'

    # def get_permissions(self):
    #     if self.action in ['signup', 'login', 'verify']:
    #         permissions = [AllowAny]
    #     elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
    #         permissions = [IsAccountOwner, IsAuthenticated]
    #     else:
    #         permissions = [IsAuthenticated]
    #     return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User registrar"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Iniciar sesion"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Felicidades, ahora puedes empezar'}
        return Response(data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['put', 'patch'])
    # def profile(self, request, *args, **kwargs):
    #     """Update profile data."""
    #     user = self.get_object()
    #     profile = user.profile
    #     partial = request.method == 'PATCH'
    #     serializer = ProfileModelSerializer(
    #         profile,
    #         data=request.data,
    #         partial=partial
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     data = UserModelSerializer(user).data
    #     return Response(data)

    # def retrieve(self, request, *args, **kwargs):
    #     """Add extra data to the response."""
    #     response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
    #     circle = Circle.objects.filter(
    #         members=request.user,
    #         membership__is_active=True
    #     )
    #     data = {
    #         'user': response.data,
    #         'circles': CircleModelSerializer(circle, many=True).data
    #     }
    #     response.data = data
    #     return response