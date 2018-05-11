from django.urls import path

from faucet import views
from web.views import app_view

urlpatterns = [
    path('', app_view, name='app'),
]