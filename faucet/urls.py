from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from faucet import views

urlpatterns = [
    path('<str:social_network>/accounts',  views.RegisterView.as_view()),
    path('<str:social_network>/<str:referrer>/accounts', views.RegisterView.as_view()),
    path('lectures', views.LectureView.as_view()),
]