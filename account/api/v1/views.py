from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer ,ChangePasswordSerializer,AddEmployeeSerializer,AddClientSerializer
from  account.models import User
from rest_framework import generics
from .permissions import IsEmployee
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
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


@api_view(["POST"])
@permission_classes([IsAdminUser])
def add_employee(request):
    response = {'data': None, 'status': status.HTTP_400_BAD_REQUEST}
    # **response -> data={},status=status.HTTP_400_BAD_REQUEST
    serializer = AddEmployeeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        response['data'] = serializer.data
        response['status'] = status.HTTP_201_CREATED
    else:
        response['data'] = serializer.errors

    return Response(**response)

@api_view(["POST"])
@permission_classes([IsEmployee])
def add_client(request):
    response = {'data': None, 'status': status.HTTP_400_BAD_REQUEST}
    # **response -> data={},status=status.HTTP_400_BAD_REQUEST
    serializer = AddClientSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        response['data'] = serializer.data
        response['status'] = status.HTTP_201_CREATED
    else:
        response['data'] = serializer.errors

    return Response(**response)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


