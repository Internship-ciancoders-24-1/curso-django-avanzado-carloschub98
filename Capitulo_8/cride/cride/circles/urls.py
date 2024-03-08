"""Urls de circulos."""

# Django
from django.urls import path, include

# Django rest framework
from rest_framework.routers import DefaultRouter

# Views
from .views import circles as circle_views
from .views.memberships import MembershipViewSet

router = DefaultRouter()
router.register(r'circles', circle_views.CircleViewSet, basename='circle')
#La r significa que recibe una expresion regular
router.register(
  r'circles/(?P<slug_name>[-a-zA-Z0-0_]+)/members',
  MembershipViewSet,
  basename='membership'
)

urlpatterns = [
    path('', include(router.urls))
]
