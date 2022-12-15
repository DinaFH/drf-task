
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    django_logout(request)
    return Response('User Logged out successfully',status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    response = {'data': None, 'status': status.HTTP_400_BAD_REQUEST}
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response['data'] = serializer.data
        response['status'] = status.HTTP_201_CREATED
    else:
        response['data'] = serializer.errors
    return Response(**response)
