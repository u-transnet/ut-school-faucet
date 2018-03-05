import datetime

from .configs import local_settings as configs
from django.db import models


class Account(models.Model):
    name = models.CharField('Аккаунт', max_length=255, unique=True)
    ip = models.CharField('IP', max_length=100, unique=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    @staticmethod
    def get_ips():
        allowedAge = datetime.datetime.now() - datetime.timedelta(seconds=configs.MIN_IP_AGE)
        return list(Account.objects.filter(created__gt=allowedAge).values_list('ip', flat=True))

    @staticmethod
    def exists(ip):
        return ip in Account.get_ips()
