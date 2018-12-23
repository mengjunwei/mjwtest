from rest_framework import serializers
from .models import Person
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(validators=[UniqueValidator(queryset=Person.objects.all())])
    user = serializers.CharField(required=False, read_only=True)
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = Person
        fields = '__all__'

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone.isdigit():
            raise serializers.ValidationError('手机号必须是数字')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if not password == password2:
            raise serializers.ValidationError('两次密码输入不一致')
        return attrs

    def create(self, validated_data):
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        email = validated_data.get('email')
        user_obj = User.objects.create_user(username=phone, password=password, email=email)
        validated_data['user'] = user_obj
        del validated_data['password']
        del validated_data['password2']
        del validated_data['email']
        instance = super(RegisterSerializer, self).create(validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = "__all__"




