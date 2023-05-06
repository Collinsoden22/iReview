from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Person, Social, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
import requests


def search_books(title):
    try:
        # Construct the API query URL
        query_url = f"https://openlibrary.org/search.json?title={title}&limit=35"
        # Send a GET request to the API
        response = requests.get(query_url)
        # Parse the JSON response
        data = response.json()
        # Extract the list of matching books from the response
        books = data["docs"]

        return books
    except Exception as e:
        return None

# Search Book using ISBN
def get_book_with_edition(edition):
    # Construct the API query URL
    query_url = f"https://openlibrary.org/books/{edition}.json"
    # Send a GET request to the API
    response = requests.get(query_url)
    # Parse the JSON response
    data = response.json()
    return data
    # Search Book using ISBN

def get_author_name(edition):
    # Construct the API query URL
    query_url = f"https://openlibrary.org/authors/{edition}.json"
    # Send a GET request to the API
    response = requests.get(query_url)
    # Parse the JSON response
    data = response.json()
    return data

def home_page_view(request, *args, **kwargs):
    return render(request, "home/index.html", {})


def community_page_view(request, *args, **kwargs):
    return render(request, "home/community.html", {})


def register_page_view(request, *args, **kwargs):
    return render(request, "registration/register.html", {})


@login_required
def profile_page_view(request, *args, **kwargs):
    user_details = Person.objects.get(username=request.user.username)
    socials = Social.objects.get(username=request.user.username)

    data = {
        "id": request.user.id,
        "username": request.user.username,
        "bio": user_details.bio,
        "image": user_details.profile_image,
        "phone_number": user_details.phone_number,
        "socials": socials
    }
    return render(request, "users/profile.html", data)


@login_required
def edit_profile_page_view(request, *args, **kwargs):
    user_details = Person.objects.get(username=request.session['username'])
    socials = Social.objects.get(username=request.session['username'])

    data = {
        "message": "Your profile has been updated",
        "id": request.user.id,
        "username": request.user.username,
        "bio": user_details.bio,
        "image": user_details.profile_image,
        "phone_number": user_details.phone_number,
        "socials": socials
    }
    return render(request, "users/edit.html", data)


def logout_user(request, *args, **kwargs):
    logout(request)
    # request.user.is_authenticated = False
    data = {
        "error": "Logged out",
        "message": "You have been logged out of iReview"
    }
    return render(request, "registration/login.html", data)


def register_user(request, *args, **kwargs):
    email = request.POST['email']
    username = request.POST['username']
    firstname = request.POST['firstName']
    lastname = request.POST['lastName']
    password = request.POST['password']

    try:
        user = User.objects.create(
            email=email, username=username, first_name=firstname, last_name=lastname
        )
        user.set_password(password)
        user.save()

        profile = Person.objects.create(username=username)
        profile.save()

        socials = Social.objects.create(username=username)
        socials.save()

        data = {
            "error": "No Errors",
            "message": "Account successfully created, Login to continue"
        }
        return render(request, "registration/login.html", data)

    except Exception as e:
        data = {
            "error": e,
            "message": "Could not process request"
        }

        return render(request, "registration/register.html", data)


def process_login_view(request, *args, **kwargs):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)

        request.session['username'] = username
        data = {
            "message": "Login Successfull",
            "id": user.id,
            "username": user.username,
        }
        # return render(request, "home/index.html", data)
        return HttpResponseRedirect("../")
    else:
        data = {
            "error": "Could not authenticate user",
            "message": "Invalid username or password, note that passwords are case sensitive"
        }
        return render(request, "registration/login.html", data)


def update_profile(request, *args, **kwargs):
    if request.method == "POST":
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        username = request.session['username']

        bio = request.POST['bio']
        phonenumber = request.POST['phoneNo']

        facebook = request.POST['facebook']
        twitter = request.POST['twitter']
        instagram = request.POST['instagram']
        linkedin = request.POST['linkedin']

        user = User.objects.filter(username=username).first()
        user.last_name = lastname
        user.first_name = firstname
        # user.save()
        try:
            if request.FILES['profileImage'].name.split(".")[-1] in ["jpg", "png", "jpeg"]:
                folder = "public/assets/img/reviewer/"
                image = request.FILES['profileImage'].name
                new_file_name = os.path.join(folder, image)
                fout = open(new_file_name, 'wb+')
                for chunk in fout.chunks:
                    fout.write(chunk)
                fout.close()
            else:
                data = {
                    "error": "Image extention error",
                    "message": "Error: Image extension not supported"
                }
                return render(request, "users/edit.html", data)
        except Exception as e:
            data = {
                "error": e,
                "message": "Could not upload profile, please select an image"
            }
            image = None
        try:
            profile = Person.objects.filter(username=user.username).first()
            if profile is not None:
                profile.bio = bio
                profile.phone_number = phonenumber
            if image is not None:
                profile.profile_image = image
            profile.save()
        except Exception as e:
            data = {
                "error": e,
                "message": "User not found, account activity suspicious"
            }

        try:
            socials = Social.objects.filter(username=username).first()
            if socials != None:
                socials.facebook = facebook
                socials.twitter = twitter
                socials.instagram = instagram
                socials.linkedin = linkedin
                socials.save()
        except Exception as e:
            data = {
                "error": e,
                "message": "Error: User not found, account activity suspicious"
            }

    user_details = Person.objects.get(username=request.session['username'])
    socials = Social.objects.get(username=request.session['username'])

    data = {
        "message": "Your profile has been updated",
        "id": user.id,
        "username": user.username,
        "bio": user_details.bio,
        "image": user_details.profile_image,
        "phone_number": user_details.phone_number,
        "socials": socials
    }
    return render(request, "users/profile.html", data)

def search_book_page(request, *args, **kwargs):
    query = request.GET.get("q")
    if query:
        books = search_books(query.replace(" ", "+"))
    else:
        books = []

    context = {
        "query": query,
        "books": books
    }
    return render(request, "home/review.html", context)


@login_required
def make_review_page(request, *args, **kwargs):
    edition = request.GET.get('q')

    book_details = get_book_with_edition(edition)
    author = get_author_name(edition)
    try:
        all_reviews = Review.objects.filter(edition=edition)
    except:
        all_reviews = None
        pass

    if all_reviews is not None:
        all_reviews = all_reviews

    data = {
        "book": book_details,
        "edition": edition,
        "author": author,
        "reviews": all_reviews
    }

    return render(request, "home/view.html", data)


def save_review(request, *args, **kwargs):
    username = request.user.username
    review = request.POST['reviewNote']
    rating = request.POST['rate']
    title = request.POST['title']
    edition = request.POST['edition']
    authors = request.POST['author']

    try:
        reviews = Review.objects.create(
            username=username, edition=edition, title=title, author=authors, review_text=review, rate=rating
        )
        reviews.save()

        return HttpResponseRedirect(f"../review?q={edition}")
    except Exception as e:
        err = "Could not complete request", e
        return HttpResponseRedirect(f"../review?err={err}&q={edition}")
