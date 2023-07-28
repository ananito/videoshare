from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .fileuploader import VideoUploadView
from .MyVideos import MyVideos

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("upload/", login_required(VideoUploadView.as_view(), redirect_field_name="login"), name="Upload"),
    path("watch", views.watch_view, name="watch"),
    path("like_dislike/<str:action>", views.like_dislike, name="like_unlike"),
    path("update_views/<str:video_id>", views.update_views, name=""),
    path("random_video/", views.random_video, name="random_video"),
    path("most_viewed/", views.most_viewed_videos, name="most_viewed"),
    path("new_comment/", views.new_comment, name="new_comment"),
    path("like_comment/", views.CommentLikes, name="comment_likes"),
    path("user/history/", views.history_view, name="history_view"),
    path("user/videos/", MyVideos.as_view(),  name="my_videos"),
    path("delete/<str:video_id>", MyVideos.as_view(),  name="my_videos"),
    path("getvideoinfo/<str:video_id>", views.getVideoInfo, name="getVideoInfor"),
    path("search", views.search_view, name="search_view")
]
