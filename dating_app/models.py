from django.db import models
from django.contrib.auth.models import User

gender_choices = (
    ('Male','Male'),
       ('Female','Female'),
       ('Others','Others')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    phone = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.ImageField(upload_to = 'profile_image/user_image',choices = gender_choices )
    looking_for = models.CharField(max_length=200, choices = gender_choices)
    # friend = models.OneToOneField('Profile',on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='image',null=True, blank=True)
    
    active = models.BooleanField(default=False)
    usercode = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.full_name
    


class Message(models.Model):
    sender = models.OneToOneField(User,on_delete=models.CASCADE,related_name='sender',null=True)
    receiver = models.OneToOneField(User,on_delete=models.CASCADE,related_name='receiver')
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/messages",
                              blank=True, null=True)
    
    def __str__(self):
        return self.content
    
    
class Chat(models.Model):
   
    participants = models.ManyToManyField(User, null = True)
    messages = models.ManyToManyField(Message, null = True)
    
    def __str__(self):
        return ''.join(self.messages.content)
    
    
    


