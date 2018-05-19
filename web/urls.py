from django.conf.urls import url
from django.urls import path

from faucet import views
from web.views import app_view, service_worker_file_view

urlpatterns = [
    url('^service-worker.js', service_worker_file_view, name='service_worker_file'),
    url('^.*', app_view, name='app'),
]