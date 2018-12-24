import binascii
import os
import time
import hashlib
import json
import datetime
from pyDes import CBC, PAD_PKCS5, des
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, field):
        if isinstance(field, datetime.datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, datetime.date):
            return field.strftime('%Y-%m-%d')
        else:
            return super(JsonCustomEncoder, self).default(field)


class CustomResponse(object):

    def __init__(self):
        self.status = False
        self.data = []
        self.message = []

    @property
    def as_json(self):
        return json.dumps(self.__dict__, cls=JsonCustomEncoder)

    @property
    def as_dict(self):
        return self.__dict__

    @property
    def as_list(self):
        return [self.status, self.data, self.message]

    @property
    def response(self):
        return Response(self.as_dict)

    def success(self, data=None, message=None):
        self.status = True
        if data:
            self.data = data
        if message:
            self.message = message
        return Response(data=self.as_dict)

    def error(self, message=None):
        if message:
            self.message = message
        return Response(data=self.as_dict)


def generate_key():
    key = "{0}_rd_{1}".format(str(time.time())[-5:], os.urandom(10))
    return hashlib.sha1(binascii.hexlify(key.encode())).hexdigest()[1:18]


def des_encrypt(s, secret_key=None):
    """对称加密"""
    secret_key = secret_key or '@mjw1234'
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    token = k.encrypt(str(s), padmode=PAD_PKCS5)
    return binascii.b2a_hex(token)


def des_descrypt(s, secret_key=None):
    """对称解密"""
    secret_key = secret_key or '@mjw1234'
    iv = secret_key
    try:
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        _decrypt = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
        username, token = _decrypt.decode().split("-")
    except:
        username, token = None, None
    return username, token


class CustomAuthBackend(BaseAuthentication):

    def authenticate(self, request):
        if request.method == "GET":
            sign = request.GET.get("token")
        elif request.method in ["POST","DELETE","PUT"]:
            sign = request.data.get("token")
        else:
            return None
        if sign:
            username, token = des_descrypt(sign)
        else:
            return None
        error = "Invalid token or username"
        try:
            if not token or not username:
                return None
            user = User.objects.get(username=username)
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User inactive or deleted.')
            if Token.objects.filter(user=user, key=token).first():
                return (user, token)
            else:
                raise exceptions.AuthenticationFailed('User token does not exist')
        except (User.DoesNotExist, Token.DoesNotExist):
            raise exceptions.AuthenticationFailed("Invalid token or username")
