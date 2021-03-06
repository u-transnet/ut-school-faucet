import datetime

from .configs import local_settings as configs
from django.db import models


class Account(models.Model):
    NETWORK_VK, NETWORK_FACEBOOK, NETWORK_GOOGLE = 'vk', 'facebook', 'google'

    NETWORKS = [
        (NETWORK_VK, 'VK'),
        (NETWORK_FACEBOOK, 'Facebook'),
        (NETWORK_GOOGLE, 'Google'),
    ]

    name = models.CharField('Аккаунт', max_length=255, unique=True)
    ip = models.CharField('IP', max_length=100, null=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    authorized_network = models.CharField('Соц. сеть', choices=NETWORKS, max_length=12, null=True)
    uid = models.CharField('UID', max_length=100, null=True)
    first_name = models.CharField('Имя', max_length=150, )
    last_name = models.CharField('Фамилия', max_length=150)
    photo = models.URLField('Фотография', max_length=255, default='')

    @staticmethod
    def get_ips():
        allowedAge = datetime.datetime.now() - datetime.timedelta(seconds=configs.MIN_IP_AGE)
        return list(Account.objects.filter(created__gt=allowedAge).values_list('ip', flat=True))

    @staticmethod
    def exists(ip):
        return ip in Account.get_ips()

    def json(self):
        return {
            'name': self.name,
            'authorized_network': self.authorized_network,
            'uid': self.uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'photo': self.photo
        }

    def __str__(self):
        return 'Аккаунт: %s' % self.name

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'
        unique_together = ('authorized_network', 'uid')


class Lecture(models.Model):
    topic_id = models.CharField('id в соц. сети', max_length=255, unique=True)
    account_name = models.CharField('Имя аккаунта', max_length=255, unique=True)

    @property
    def topic_url(self):
        return 'https://vk.com/topic-%s' % self.topic_id

    def json(self):
        return {
            'topic_url': self.topic_url,
            'account_name': self.account_name
        }

    def __str__(self):
        return self.topic_url

    class Meta:
        verbose_name = 'лекция'
        verbose_name_plural = 'лекции'
