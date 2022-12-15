from django.urls import path ,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import ChangePasswordView
from .views import logout,signup
app_name='account-rest-v1'
urlpatterns=[
    path('rest-login',obtain_auth_token),
    path('logout', logout, name="logout"),
    path('signup',signup,name='signup'),
    path('change-password',ChangePasswordView.as_view(),name='change-password'),
    path('reset-password', include('django_rest_passwordreset.urls', namespace='password_reset')),
]