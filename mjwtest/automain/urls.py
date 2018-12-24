from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexApiView.as_view(), name='index'),
    path('login/', LoginApiView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('register/', ResigterApiView.as_view(), name="register"),
    path('users/', UserApiView.as_view(), name="user_list")
]