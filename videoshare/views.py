from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserRegistrationForm, LoginForm

# Create your views here.

def index(request):
    return render(request, "videoshare/index.html")

def register(request):
    if request.method == "POST":

        # Send Request data to the form
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)        

        return HttpResponseRedirect(reverse("index"))

    else:
        if request.user.is_authenticated:
            logout(request)

        return render(request, "videoshare/register.html", {
        "form": UserRegistrationForm(),
        }) 

def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            
            # Attempt to sign user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "videoshare/login.html")
    else:
        # The users shouldnt be logged in
        if request.user.is_authenticated:
            logout(request)
        
        form = LoginForm()
        return render(request, "videoshare/login.html", {
            "form": form
        })
