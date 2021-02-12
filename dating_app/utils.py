from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Chat, Profile

User = get_user_model()




def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Profile, user=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)
