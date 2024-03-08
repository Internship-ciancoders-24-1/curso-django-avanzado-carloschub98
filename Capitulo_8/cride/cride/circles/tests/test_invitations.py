

"""Invitations tests."""

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Model
from cride.circles.models import Circle, Invitation, Membership
from cride.users.models import User, Profile
from rest_framework.authtoken.models import Token


class InvitationsManagerTestCase(TestCase):
    """Testeando la invitacion de un miembro"""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Franklin',
            last_name='Garcia',
            email='fm-garcia@outlook.com',
            username='fmgarcia',
            password='admin123'
        )
        self.circle = Circle.objects.create(
            name='Computer Science Faculty',
            slug_name='csfaculty',
            about="Official UPC's Computer Science Faculty",
            verified=True
        )

    def test_code_generation(self):
        """Los códigos aleatorios deben generarse automáticamente."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """Si se proporciona un código, no es necesario crear uno nuevo."""
        code = 'TESTCODE01'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """Si el código dado no es único, se debe generar uno nuevo."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )

        self.assertNotEqual(code, invitation.code)


class MemberInvitationsAPITestCase(APITestCase):
    """Caso de prueba de API de invitación de miembros."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Franklin',
            last_name='Garcia',
            email='fmgarcia@outlook.com',
            username='fmgarcia',
            password='admin123'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create(
            name='Computer Science Faculty',
            slug_name='csfaculty',
            about="Official UPC's Computer Science Faculty",
            verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        # URL
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )

    def test_response_success(self):
        """Verificando que la solicitud sea de exito"""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Se generan invitaciones de verificación si no existe ninguna anteriormente."""
        # Las invitaciones en DB deben ser 0
        self.assertEqual(Invitation.objects.count(), 0)

        # URL de invitaciones para miembros de llamadas
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verificar que se crearon nuevas invitaciones
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
