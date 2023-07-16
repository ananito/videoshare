from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .fileuploader import VideoUploadView

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("upload/", login_required(VideoUploadView.as_view(), redirect_field_name="login"), name="Upload"),
    path("watch", views.watch_view, name="watch"),
    path("like_dislike/<str:action>", views.like_dislike, name="like_unlike")
]
