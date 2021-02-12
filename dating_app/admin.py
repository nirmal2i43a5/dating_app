from django.contrib import admin

from .models import Profile, Chat, Message

admin.site.register(Chat)
admin.site.register(Profile)
admin.site.register(Message)
