from django.contrib import admin
from .models import Profile, Job, Application

admin.site.register([Profile, Job, Application])
