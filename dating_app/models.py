from django.db import models

# Create your models here.
class User(models.Model):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)
    avatar = models.ImageField(upload_to='image',null=True, blank=True)
    active = models.BooleanField(default=False)
    usercode = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

class Message(models.Model):
    sender = models.OneToOneField(User,on_delete=models.CASCADE)
    receiver1 = models.OneToOneField(User,on_delete=models.CASCADE)

class Contact(models.Model):
    pass