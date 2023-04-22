from django.contrib import admin

# Register your models here.
from review.models import *

admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Social)
