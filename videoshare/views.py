from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "videoshare/index.html")

def register(request):
   if request.method == "POST":
    pass
   elif request.method == "GET":
       return render(request, "videoshare/register.html") 
