from django.contrib import admin
from .models import PersonalChats, Friends, ImageUpload
# Register your models here.

admin.site.register(PersonalChats)
admin.site.register(Friends)
admin.site.register(ImageUpload)