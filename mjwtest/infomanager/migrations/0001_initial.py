# Generated by Django 2.1.4 on 2019-05-12 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('pub_date', models.DateField(null=True, verbose_name='发布日期')),
                ('readcount', models.IntegerField(default=0, verbose_name='阅读量')),
                ('commentcount', models.IntegerField(default=0, verbose_name='评论量')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
            ],
            options={
                'verbose_name': '图书',
                'db_table': 'bookinfo',
            },
        ),
    ]
