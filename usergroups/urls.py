from django.urls import path
from . import views

urlpatterns = [
    path('<groupname>/', views.GroupCreate, name = 'GroupCreate'),
    path('<groupname>/chats/', views.GroupView, name = 'GroupView'),
    path('<name>/participants/', views.Participants, name = 'Participants'),
    path('<name>/info/', views.GroupInfo, name = 'GroupInfo'),
]