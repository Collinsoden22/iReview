from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=45)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Person(models.Model):
    username = models.CharField(max_length=30)
    bio = models.CharField(max_length=255, NULL=True)
    profile_image = models.CharField(max_length=255, NULL=True)