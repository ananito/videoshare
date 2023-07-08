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

        return render(request, "videoshare/register.html", {
        "form": form,
        }) 
    else:
        if request.user.is_authenticated:
            logout(request)

        return render(request, "videoshare/register.html", {
        "form": UserRegistrationForm(),
        }) 

