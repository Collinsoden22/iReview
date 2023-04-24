"""ireview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
"""
from django.contrib import admin
from django.urls import path, include
from review.views import *

urlpatterns = [
    path('', home_page_view),
    path('community/', community_page_view),
    path('profile/', profile_page_view),
    path('profile/edit', edit_profile_page_view),
    path('update-profile/', update_profile),
    path('process-login', process_login_view),
    path('search/', search_book_page),
    path('send-review/', save_review),
    path('review/', make_review_page),
    path('register/', register_page_view),
    path('create-account/', register_user),
    path('accounts/logout/', logout_user),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
