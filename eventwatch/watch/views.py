from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "watch/index.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "watch/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "watch/login.html")

def user_logout(request):
    logout(request)
    return render(request, "watch/login.html", {
        "message": "Logged out!"
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]

        # Basic validation for empty fields and password matching
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "watch/register.html")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "watch/register.html")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "watch/register.html")

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Log the user in and redirect to the home page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "watch/register.html")
