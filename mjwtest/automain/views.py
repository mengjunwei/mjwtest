from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import  CreateAPIView, ListAPIView
from .serializers import RegisterSerializer, UserSerializer
from .models import Person
# Create your views here.


class ResigterApiView(CreateAPIView):
    serializer_class = RegisterSerializer


class UserApiView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = UserSerializer



def index(request):
    return JsonResponse({"msg":'guopenghua my wife'})
