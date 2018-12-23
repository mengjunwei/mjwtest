from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Person(models.Model):
    SEX_CHOICES = (
        ("man", "男"),
        ("woman", "女")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='手机号', max_length=11)
    age = models.IntegerField(verbose_name="年龄")
    sex = models.CharField(verbose_name="性别", choices=SEX_CHOICES, max_length=16)
    birthday = models.DateTimeField(verbose_name="生日")

    def __str__(self):
        return self.phone

