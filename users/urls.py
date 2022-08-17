from django.contrib import admin
from django.urls import include, path

from .views import LogInView, LogOutView, RegisterView, UserView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LogInView.as_view()),
    path("user/", UserView.as_view()),
    path("logout/", LogOutView.as_view()),
]
