from django.db import models
from django.core.files.storage import FileSystemStorage


# Create your models here
class Users(models.Model):
    username = models.CharField(unique=True, max_length = 20)
    password = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 40)
    profilepic = models.TextField(default='-')
    about = models.TextField(default='-')
