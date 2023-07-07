from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserForm

# Create your views here.

def index(request):
    return render(request, "videoshare/index.html")

def register(request):

   if request.method == "POST":

    # Send Request to the form
    form = UserForm(request.POST)

    try:
        if form.is_valid():

            user = form.save()
    except ValidationError as e:

        return render(request, "videoshare/register.html", {
        "form": UserForm(),
        "message": e
       }) 


    login(request, user)
    return HttpResponseRedirect(reverse("index"))


   elif request.method == "GET":
       return render(request, "videoshare/register.html", {
        "form": UserForm(),
       }) 
