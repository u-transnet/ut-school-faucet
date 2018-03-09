from django.urls import path

from faucet import views

urlpatterns = [
    path('accounts', views.AccountView.as_view(), name='accounts'),
    path('lectures', views.LectureView.as_view(), name='lectures'),
]