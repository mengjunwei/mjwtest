from django.db import models

# Create your models here.


class ApiLog(models.Model):
    event_id = models.CharField('调用事件标志', max_length=100, null=True, blank=True)
    remote_hostname = models.CharField('调用主机', max_length=100, null=True, blank=True)
    remote_address = models.GenericIPAddressField('调用主机IP', null=True, blank=True)
    username = models.CharField('用户名', max_length=100, null=True, blank=True)
    request_path = models.TextField('请求接口路径', null=True, blank=True)
    request_method = models.CharField('请求方法', max_length=10, null=True, blank=True)
    request_body = models.TextField('请求body', null=True, blank=True)
    response_code = models.CharField('返回code', max_length=10, null=True, blank=True)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')

    def __unicode__(self):
        return '%s:%s' % (self.remote_address, self.request_path)

    class Meta:
        verbose_name = '接口调用日志'
        verbose_name_plural = '接口调用日志'