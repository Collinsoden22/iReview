from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.


def home_page_view(request, *args, **kwargs):
    return render(request, "home/index.html", {})


def community_page_view(request, *args, **kwargs):
    return render(request, "home/community.html", {})


def register_page_view(request, *args, **kwargs):
    return render(request, "registration/register.html", {})

def register_user(request, *args, **kwargs):
    email = request.POST['email'];
    username = request.POST['username'];
    firstname = request.POST['firstName'];
    lastname = request.POST['lastName'];
    password = request.POST['password'];

    try:
        user_data = User.objects.create(email=email, username=username, first_name=firstname, last_name=lastname, password=password)
        user_data.save()
    except Exception as e:
        return {
            "error" : e,
            "message": "Could not process request"
        }

    return render(request, "registration", request.POST)