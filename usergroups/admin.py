from django.contrib import admin
from .models import Groups, GroupUsers, GroupChats, ImageUploadGroup

admin.site.register(Groups)
admin.site.register(GroupUsers)
admin.site.register(GroupChats)
admin.site.register(ImageUploadGroup)
