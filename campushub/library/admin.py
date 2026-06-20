from django.contrib import admin
from .models import Author, Book, Member, Issue

admin.site.register([Author, Book, Member, Issue])
