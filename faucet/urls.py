from django.urls import path

from faucet import views

urlpatterns = [
    path('<str:social_network>/accounts',  views.RegisterView.as_view()),
    path('lectures', views.LectureView.as_view()),
]