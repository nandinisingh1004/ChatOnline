from django.db import models
from django.contrib.auth.models import User

class Friends(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'firstfriend')
    friend = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'secondfriend')

    class Meta:
        verbose_name_plural = 'Friends'

class PersonalChats(models.Model):
    friend = models.ForeignKey(Friends, on_delete = models.CASCADE, related_name='friends')
    chat = models.TextField(default='-')
    time = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length = 20, default='-')
    msgtype = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'PersonalChats'

class ImageUpload(models.Model):
    path_image = models.TextField()
    filename = models.TextField()
    chatconnect = models.ForeignKey(Friends, on_delete = models.CASCADE, related_name='sentimages')
    time = models.DateTimeField(auto_now_add=True)
    msgtype = models.IntegerField(default=0)
    sender = models.CharField(max_length = 20, default='-')
    class Meta:
        verbose_name_plural = 'ImageUploads'
    

