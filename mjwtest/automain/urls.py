from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', ResigterApiView.as_view(), name="register"),
    path('users/', UserApiView.as_view(), name="user_list")
]