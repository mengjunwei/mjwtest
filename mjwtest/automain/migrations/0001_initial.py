# Generated by Django 2.1.4 on 2018-12-23 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('sex', models.CharField(choices=[('man', '男'), ('woman', '女')], max_length=16, verbose_name='性别')),
                ('birthday', models.DateTimeField(verbose_name='生日')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
