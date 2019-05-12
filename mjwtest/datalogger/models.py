from django.db import models

# Create your models here.


class Datalogger(models.Model):
    event_id = models.CharField(u'事件ID', max_length=100, blank=True, null=True)
    type_choices = (('delete', u'删除'),
                    ('add', u'新增'),
                    ('update', u'更新'))
    event_type = models.CharField(u'事件类型', choices=type_choices, max_length=10, blank=True, null=True)
    object_id = models.IntegerField(u'数据ID', blank=True, null=True)
    model_name = models.CharField(u'修改对象名称', max_length=100, blank=True, null=True)
    field_name = models.CharField(u'修改的字段名称', max_length=100, blank=True, null=True)
    before_value = models.TextField(u'修改前的值', blank=True, null=True)
    after_value = models.TextField(u'修改后的值', blank=True, null=True)
    operator = models.CharField(u'操作人', max_length=100, blank=True, null=True)
    create_at = models.DateTimeField(blank=True, auto_now_add=True)
    update_at = models.DateTimeField(blank=True, auto_now=True)

    def __str__(self):
        return '%s - %s - %s' % (self.event_id, self.model_name, self.field_name)

    class Meta:
        verbose_name = '日志记录'
