from django.urls import path ,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ChangePasswordView
from .views import logout,signup,add_employee
app_name='account-rest-v1'
urlpatterns=[
    path('rest-login',obtain_auth_token),
    path('logout', logout, name="logout"),
    path('signup',signup,name='signup'),
    path('change-password',ChangePasswordView.as_view(),name='change-password'),
    path('add-employee',add_employee,name='add-employee'),

]