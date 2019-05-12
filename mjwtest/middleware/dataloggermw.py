# -*- coding:utf-8 -*-
from django.apps import apps
import socket
import datetime
import uuid
import logging
from django.utils.deprecation import MiddlewareMixin

from api import models as api_models
from datalogger import globals

logger = logging.getLogger('cmdbapp')


class ApiLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = datetime.datetime.now()
        request.api_user = request.REQUEST.get('username')
        request.event_id = request.REQUEST.get('event_id', '')
        request._body_to_log = request.body
        logger.info('[%s]调用接口，请求id[%s]' % (request.api_user, request.event_id))

    def process_response(self, request, response):
        log_data = {
            'username': request.api_user,
            'remote_address': request.META['REMOTE_ADDR'],
            'remote_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            'request_body': '' if 'api/v1.0' in request.get_full_path() else request._body_to_log,
            'response_code': response.status_code,
            'event_id': request.event_id if hasattr(request, 'event_id') else '',
            'start_time': request.start_time,
            'end_time': datetime.datetime.now(),
        }
        api_models.ApiLog.objects.create(**log_data)
        logger.info('记录接口日志数据：%s' % log_data)
        return response


class DataUpadataDeleteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        根据配置url的models列表，给model打event_id 和 operator
        """
        globals.event_id = uuid.uuid1()
        globals.username = request.user.username

