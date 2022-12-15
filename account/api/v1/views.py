
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.contrib.auth import logout as django_logout
from rest_framework.response import Response

from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    django_logout(request)
    return Response('User Logged out successfully',status=status.HTTP_200_OK)
