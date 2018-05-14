from django.conf.urls import url
from django.urls import path

from faucet import views
from web.views import app_view

urlpatterns = [
    url('^.*', app_view, name='app'),
]