from rest_framework import serializers

from dating_app.models import Chat, Message
from dating_app.utils import get_user_contact



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Message
        fields = ('content',)


class MessageSerializer(serializers.ModelSerializer):
    # content = MessageSerializer(required = True)
    # participants = ContactSerializer(many=True)

    class Meta:
        model = Message
        fields = ('to','content',)
        # fields = ('id', 'content', 'participants')
        # read_only = ('id')
        # lookup_field = 'messages'

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            profile = get_user_contact(username)
            chat.participants.add(profile)
        chat.save()
        return chat
    
class ChatSerializer(serializers.ModelSerializer):
    # content = MessageSerializer(required = True)
    # participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        # fields = ('sender','receiver','content',)
        fields = ('id', 'messages', 'participants')
      

    def create(self, validated_data):
        print(validated_data)
        participants = validated_data.pop('participants')
        chat = Chat()
        chat.save()
        for username in participants:
            profile = get_user_contact(username)
            chat.participants.add(profile)
        chat.save()
        return chat


# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
