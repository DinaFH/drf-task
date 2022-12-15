from django.urls import path ,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ChangePasswordView
from .views import logout,signup,add_employee,add_client,list_users,user_details,update_user,delete_user
app_name='account-rest-v1'
urlpatterns=[
    path('rest-login',obtain_auth_token),
    path('logout', logout, name="logout"),
    path('signup',signup,name='signup'),
    path('change-password',ChangePasswordView.as_view(),name='change-password'),
    path('add-employee',add_employee,name='add-employee'),
    path('add-client',add_client,name='add-client'),
    path('list-users', list_users, name='list'),
    path('user-details/<int:user_id>', user_details, name='detail'),
    path('update-user/<int:user_id>', update_user, name='update'),
    path('delete-user/<int:user_id>', delete_user, name='delete'),



]