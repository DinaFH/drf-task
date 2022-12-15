from rest_framework.permissions import BasePermission
from account.models import User



class IsEmployee(BasePermission):
    def has_permission(self, request, view):

        if request.user.type=='employee':
            return True
        else:
            return False