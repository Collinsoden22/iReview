from django.db import models
from datetime import date

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


class Person(models.Model):
    username = models.CharField(max_length=30, unique=True)
    bio = models.CharField(max_length=255, null=True)
    profile_image = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=12, null=True)


class Social(models.Model):
    username = models.CharField(max_length=30, unique=True)
    facebook = models.CharField(max_length=30, null=True)
    instagram = models.CharField(max_length=30, null=True)
    twitter = models.CharField(max_length=30, null=True)
    linkedin = models.CharField(max_length=30, null=True)


class Review(models.Model):
    username = models.CharField(max_length=30)
    isbn = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=46)
    review_text = models.TextField()
    review_date = models.DateField(default=date.today)
