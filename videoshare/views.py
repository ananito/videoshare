from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models.functions import Random
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm

from .models import VideoUpload

# Create your views here.


def index(request):
    videos = VideoUpload.objects.filter(private=False).order_by(Random())[:30]

    return render(request, "index.html", {
        "videos": videos
    })


def register(request):
    if request.method == "POST":

        # Send Request data to the form
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse("index"))

        return render(request, "register.html", {
            "form": form,
        })
    else:
        if request.user.is_authenticated:
            logout(request)

        return render(request, "register.html", {
            "form": UserRegistrationForm(),
        })


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
    
    recommends = VideoUpload.objects.filter(private=False).order_by(Random())[:25]

    return render(request, "watch.html", {
        "video": video,
        "recommends": recommends
    })
