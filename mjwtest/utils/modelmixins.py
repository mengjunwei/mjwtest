# -*- coding:utf-8 -*-
from django.db import models
from django.forms.models import model_to_dict
import logging
from datalogger.models import Datalogger
from datalogger import globals

logger = logging.getLogger('utils')


class ModelDiffMixin(object):
    """
    model 获取变更字段扩展
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                                           self._meta.fields if field.name != 'id'])


class LogOnUpdateDeleteModel(ModelDiffMixin, models.Model):
    """
    重写 model 方法，记录日志操作
    """

    def delete(self, *args, **kwargs):
        logger.info('记录delete日志')
        if hasattr(globals, 'event_id'):
            for key, value in model_to_dict(self, fields=[field.name for field in self._meta.fields if
                                                          field.name != 'id']).items():
                dataloger = {'event_id': globals.event_id, 'event_type': 'delete',
                             'model_name': self._meta.model.__name__, 'object_id': self.pk,
                             'field_name': key, 'before_value': value, 'operator': globals.username}
                logger.info('删除数据：%s' % dataloger)
                Datalogger.objects.create(**dataloger)
        else:
            logger.info('请求没有 event_id 字段，不记录日志')
        super(LogOnUpdateDeleteModel, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        logger.info('记录save日志')
        is_post = False
        # 更新
        if self.pk:
            logger.info('更新---|')
            if not hasattr(globals, 'event_id'):
                logger.info('请求没有 event_id 字段，不记录日志')
            elif not self.changed_fields:
                logger.info('请求没有字段变化，不记录日志')
            else:
                dataloger = {}
                dataloger['event_id'] = globals.event_id  # self.log_event_id
                dataloger['event_type'] = 'update'
                dataloger['model_name'] = self._meta.model.__name__
                dataloger['object_id'] = self.pk
                for name in self.changed_fields:
                    dataloger['field_name'] = name
                    before = self.get_field_diff(name)[0]  # (变化前的值，变化后的值)
                    after = self.get_field_diff(name)[1]  # (变化前的值，变化后的值)
                    dataloger['before_value'] = before
                    dataloger['after_value'] = after
                    dataloger['operator'] = globals.username  # self.log_operator
                    Datalogger.objects.create(**dataloger)
                    logger.info('记录数据：%s' % dataloger)
                    # 判定是否需要事件推送
                    if 'hostname' == name and self._meta.model.__name__ == 'Asset':
                        is_post = True
                    # if 'usage' == name and self._meta.model.__name__ == 'Asset':
                    #     # 待优化
                    #     post_event.send(self, action='update', modify='usage')  # 向别的系统推送状态更新信息


            super(LogOnUpdateDeleteModel, self).save(*args, **kwargs)
            # # 事件推送
            # if is_post:
            #     post_event.send(self, action='update')  # 向别的系统推送状态更新信息
        else:
            logger.info('新增---|')
            super(LogOnUpdateDeleteModel, self).save(*args, **kwargs)
            # 新增
            if hasattr(globals, 'event_id'):
                for key, value in model_to_dict(self, fields=[field.name for field in self._meta.fields if
                                                              field.name != 'id']).items():
                    dataloger = {'event_id': globals.event_id, 'event_type': 'add',
                                 'model_name': self._meta.model.__name__, 'object_id': self.pk,
                                 'field_name': key, 'after_value': value, 'operator': globals.username}
                    Datalogger.objects.create(**dataloger)
                    logger.info('新增数据记录：%s' % dataloger)
            else:
                logger.info('请求没有 event_id 字段，不记录日志')

    class Meta:
        abstract = True
