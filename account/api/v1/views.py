from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.contrib.auth import logout as django_logout
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer ,ChangePasswordSerializer,AddEmployeeSerializer,AddClientSerializer,UserSerializer,UserUpdateSerializer
from  account.models import User
from rest_framework import generics
from .permissions import IsEmployee ,IsOwner
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated ,IsAdminUser



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

@api_view(['GET'])
def list_users(request):
    users = User.objects.all().exclude(id=1)
    serializer = UserSerializer(users, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_details(request, user_id):
    response = {'data': {}, 'status': status.HTTP_204_NO_CONTENT}
    try:
        if user_id != 1:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user, many=False)
            response['data'] = serializer.data
            response['status'] = status.HTTP_200_OK
        else:
            response['data'] = {'no content'}
            response['status'] = status.HTTP_200_OK
    except ObjectDoesNotExist:
        response['data'] = {'no content'}
        response['status'] = status.HTTP_204_NO_CONTENT
    except:
        response['data'] = {'internal server error'}
        response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return Response(**response)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsOwner])
def update_user(request, user_id):
    response = {'data': {}, 'status': status.HTTP_204_NO_CONTENT}
    user_instance = User.objects.get(id=user_id)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(instance=user_instance, data=request.data)
    else:
        serializer = UserUpdateSerializer(instance=user_instance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        response['data'] = serializer.data['username']
        response['status'] = status.HTTP_200_OK
    else:
        response['data'] = serializer.errors
        response['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, **kwargs):
    user_id = kwargs.get('user_id')
    User.objects.get(pk=user_id).delete()
    return Response(data={'detail': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

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


