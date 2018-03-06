from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from faucet import views

urlpatterns = [
    path('<str:social_network>/accounts',  csrf_exempt(views.RegisterView.as_view())),
    path('<str:social_network>/<str:referrer>/accounts', csrf_exempt(views.RegisterView.as_view())),
    path('lectures', csrf_exempt(views.LectureView.as_view())),
]