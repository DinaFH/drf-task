from rest_framework.permissions import BasePermission
from account.models import User

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        current_id = int(user.id)
        url_id = int(request.path.split('/')[5])
        if(current_id == url_id):
            return True
        else:
            return False

class IsEmployee(BasePermission):
    def has_permission(self, request, view):

        if request.user.type=='employee':
            return True
        else:
            return False