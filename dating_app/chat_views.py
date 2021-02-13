from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import  generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)

from dating_app.models import Chat
from dating_app.utils import get_user_contact
from .chat_serializers import ChatSerializer, MessageSerializer

User = get_user_model()

class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset
    
    


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )




        
class ChatCreateView(CreateAPIView):
    # queryset = Chat.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = (permissions.IsAuthenticated, )

      
    def post(self, request, *args, **kwargs):
       
        data = request.data
        serializer = MessageSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        
        #if invalid
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    



class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )



# class ChatUpdateView(CreateAPIView):
#     # queryset = Chat.objects.all()
#     serializer_class = MessageSerializer
#     # permission_classes = (permissions.IsAuthenticated, )



class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )
