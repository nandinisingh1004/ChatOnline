from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterView, name = 'RegisterView'),
    path('logout/', views.LogoutView, name = 'LogoutView'),
    path('extrainfo/', views.SaveProfilePic, name = 'SaveProfilePic'),
    path('login/', views.LoginView, name = 'LoginView'),
]