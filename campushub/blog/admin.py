from django.contrib import admin
from .models import Category, Post, Comment

admin.site.register([Category, Post, Comment])
