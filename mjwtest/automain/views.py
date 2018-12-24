from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import CustomResponse, generate_key, des_encrypt, CustomAuthBackend
from rest_framework.views import APIView
from rest_framework.generics import  CreateAPIView, ListAPIView
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Person
# Create your views here.


class LoginApiView(APIView):

    def post(self, request):
        result = CustomResponse()
        phone = request.data.get('phone')
        pwd = request.data.get('pwd')
        update = request.data.get("update", False)
        user = authenticate(username=phone, password=pwd)
        login(request, user=user)

        if user:
            tokenobj = Token.objects.filter(user=user)
            token = generate_key()
            if not tokenobj:
                Token.objects.create(user=user, key=token)
            else:
                if update:
                    tokenobj.update(key=token)
                else:
                    token = tokenobj.first().key
            sign = "{0}-{1}".format(user.username, token)
            result.data = {"token": des_encrypt(sign), "username": user.username}
            result.status = True
        else:
            result.message = "Wrong username or password!"
        return result.response


class LogoutApiView(APIView):

    def get(self, request):
        result = CustomResponse()
        user = request.user
        Token.objects.filter(user=user).delete()
        logout(request)
        result.message = "退出登录成功"
        result.status = True
        return result.response


class ResigterApiView(CreateAPIView):
    serializer_class = RegisterSerializer


class UserApiView(LoginRequiredMixin, ListAPIView):
    authentication_classes = (CustomAuthBackend,)
    permission_classes = (IsAuthenticated,)
    queryset = Person.objects.all()
    serializer_class = UserSerializer



class IndexApiView(APIView):

    def get(self, request, *args, **kwargs):

        response = CustomResponse()
        return response.success(data={"msg":'test'})

