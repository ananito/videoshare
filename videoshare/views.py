import json
import random
import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta
from django.core import serializers
from django.db.models.functions import Random
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm
from .models import Comment, CommentLike, Like, UserViewHistory, VideoUpload

# from django.utils import timezone


# Create your views here.


def index(request):
    videos = VideoUpload.objects.filter(private=False).order_by(Random())[:30]

    return render(request, "index.html", {"videos": videos})


def register(request):
    if request.method == "POST":
        # Send Request data to the form
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        return render(
            request,
            "register.html",
            {
                "form": form,
            },
        )
    else:
        if request.user.is_authenticated:
            logout(request)

        return render(
            request,
            "register.html",
            {
                "form": UserRegistrationForm(),
            },
        )


def watch_view(request):
    video_id = request.GET.get("v")
    if not video_id:
        return HttpResponseRedirect(reverse("index"))

    if len(video_id) != 8:
        raise Http404("Page does not exist")

    try:
        video = VideoUpload.objects.get(video_id=video_id)
    except VideoUpload.DoesNotExist:
        raise Http404("Page does not exist")

    likes_dislikes = Like.objects.get_or_create(video=video)[0]

    recommends = (
        VideoUpload.objects.filter(private=False)
        .order_by(Random())
        .exclude(video_id=video_id)[:25]
    )

    comments = Comment.objects.filter(video=video).order_by("-likes", "-created_at")

    return render(
        request,
        "watch.html",
        {
            "video": video,
            "recommends": recommends,
            "likes": likes_dislikes,
            "comments": comments,
        },
    )


@login_required(redirect_field_name="login")
def like_dislike(request, action):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required"}, status=400)

    data = json.loads(request.body)
    unique_id = data.get("unique_id")
    video_id = data.get("video_id")
    username = request.user.username

    try:
        uuid.UUID(str(unique_id))
    except ValueError:
        return JsonResponse({"message": "Invalid unique_id "}, status=400)

    try:
        video = VideoUpload.objects.get(unique_id=unique_id, video_id=video_id)
    except VideoUpload.DoesNotExist:
        return JsonResponse({"message": "Invalid video id or unique_id "}, status=400)

    try:
        like_dislike = Like.objects.get(video=video)
    except Like.DoesNotExist:
        return JsonResponse({"message": "error "}, status=400)

    if action == "like":
        if like_dislike.liked_by.filter(username=username).exists():
            like_dislike.liked_by.remove(request.user)
            like_dislike.save()
        else:
            like_dislike.liked_by.add(request.user)
            like_dislike.disliked_by.remove(request.user)
            like_dislike.save()
    elif action == "dislike":
        if like_dislike.disliked_by.filter(username=username).exists():
            like_dislike.disliked_by.remove(request.user)
            like_dislike.save()
        else:
            like_dislike.disliked_by.add(request.user)
            like_dislike.liked_by.remove(request.user)
            like_dislike.save()
    else:
        return Http404("Url Does not exists!")
    return JsonResponse(
        {
            "message": {
                "like": like_dislike.liked_by.count(),
                "dislike": like_dislike.disliked_by.count(),
            }
        },
        status=200,
    )


def update_views(request, video_id):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required"}, status=400)

    data = json.loads(request.body)

    if data.get("video_id") != str(video_id):
        return JsonResponse({"message": "video id did not match"}, status=400)

    try:
        video = VideoUpload.objects.get(video_id=data.get("video_id"))
    except VideoUpload.DoesNotExist:
        return JsonResponse({"message": "invalid video id"}, status=400)

    if request.user.is_authenticated:
        try:
            userhistory = UserViewHistory.objects.get(user=request.user)
            userhistory.videos.add(video)
            video.views += 1
            video.save()
            userhistory.save()
        except UserViewHistory.DoesNotExist:
            userhistory = UserViewHistory.objects.create(user=request.user)
            video.views += 1
            video.save()
    elif not request.user.is_authenticated:
        video.views += 1
        video.save()

    return JsonResponse({"message": "success"}, status=200)


def random_video(self):
    video_count = VideoUpload.objects.filter(private=False).order_by(Random())[:50]
    rand_num = random.randint(0, (video_count.count() - 1))
    video = video_count[rand_num]
    return HttpResponseRedirect(reverse("watch") + f"?v={video.video_id}")
    # return HttpResponse(f"{random.randint(0, video_count-1)}")


def most_viewed_videos(request):
    videos = VideoUpload.objects.filter(private=False).order_by("-views")
    return render(request, "most_viewed_videos.html", {"videos": videos})


def new_comment(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required"}, status=400)

    data = json.loads(request.body)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "User Should be signed in"}, status=400)

    try:
        video = VideoUpload.objects.get(video_id=data.get("video_id"))
    except VideoUpload.DoesNotExist:
        return JsonResponse({"message": "invalid video id"}, status=400)

    if data.get("commentBody") == "":
        return JsonResponse({"error": "please insert a text"}, status=400)

    if str(data.get("commentBody")).isspace():
        return JsonResponse({"error": "please insert a text"}, status=400)

    try:
        comment = Comment.objects.create(
            user=request.user, video=video, comment=data.get("commentBody")
        )
    except Comment.IntegrityError:
        return JsonResponse({"error": "Something went wrong"}, status=400)

    return JsonResponse(
        {
            "message": "success",
            "data": {
                "id": comment.id,
                "username": comment.user.username,
                "body": comment.comment,
                "likes": comment.likes,
                "created_at": comment.created_at,
            },
        },
        status=200,
    )


def CommentLikes(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required"}, status=400)

    data = json.loads(request.body)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "User Should be signed in"}, status=400)

    try:
        VideoUpload.objects.get(video_id=data.get("video_id"))
    except VideoUpload.DoesNotExist:
        return JsonResponse({"message": "invalid video id"}, status=400)

    try:
        comment = Comment.objects.get(pk=data.get("comment_id"))
    except Comment.DoesNotExist:
        return JsonResponse({"message": "invalid comment id"}, status=400)

    try:
        comment_like = CommentLike.objects.get(comment=comment)
        if request.user in comment_like.user.all():
            comment_like.user.remove(request.user)
            comment_like.save()
            comment.likes -= 1
            comment.save()
        else:
            comment_like.user.add(request.user)
            comment_like.save()
            comment.likes += 1
            comment.save()
    except CommentLike.DoesNotExist:
        comment_like = CommentLike.objects.create(comment=comment)
        comment_like.user.add(request.user)
        comment_like.save()
        comment.likes += 1
        comment.save()

    return JsonResponse(
        {"message": "success", "data": {"total": comment_like.user.count()}}, status=200
    )


@login_required(redirect_field_name="login")
def history_view(request):
    try:
        history = UserViewHistory.objects.get(user=request.user)
    except UserViewHistory.DoesNotExist:
        return render(request, "history.html", {"histories": False})

    return render(
        request, "history.html", {"histories": history.videos.order_by("-date")}
    )


@login_required(redirect_field_name="login")
def getVideoInfo(request, video_id):
    if request.method != "GET":
        return JsonResponse({"message": "GET request required"}, status=400)

    video = VideoUpload.objects.filter(video_id=video_id)
    if not video.exists():
        return JsonResponse({"message": "invalid video id"}, status=400)

    obj = serializers.serialize("json", video)
    return HttpResponse(obj, content_type="application/json")


def search_view(request):

    query = request.GET.get("q")
    videos = VideoUpload.objects.filter(title__contains=query, private=False).order_by("-views", "-date")
    return render(request, "search.html", {"query": query, "videos": videos})
