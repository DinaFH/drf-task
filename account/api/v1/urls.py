from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import logout,signup
app_name='account-rest-v1'
urlpatterns=[
    path('rest-login',obtain_auth_token),
    path('logout', logout, name="logout"),
    path('signup',signup,name='signup'),
]