from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from faucet import views

urlpatterns = [
    path('accounts',  csrf_exempt(views.RegisterView.as_view())),
    path('<str:referrer>/accounts', csrf_exempt(views.RegisterView.as_view())),
]