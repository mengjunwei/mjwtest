from django.db import models
from django.contrib.auth.models import User
from utils.modelmixins import LogOnUpdateDeleteModel

# Create your models here.


class Person(LogOnUpdateDeleteModel):
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


class PersonPosition(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    position = models.CharField(max_length=256, verbose_name='职位')

    def __str__(self):
        return '{}-{}'.format(self.person.user.username, self.position)
