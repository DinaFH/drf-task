from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import logout
app_name='account-rest-v1'
urlpatterns=[
    path('rest-login',obtain_auth_token),
   # path('signup',signup,name='signup'),
    path('logout', logout, name="logout"),
]