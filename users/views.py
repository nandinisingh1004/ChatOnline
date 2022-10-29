from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Users
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core import serializers

# Create your views here.
def RegisterView(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:
            hashed_pwd = make_password(password1)
            Users.objects.create(username = uname, email = email , password = hashed_pwd)
            user = User.objects.create_user(username=uname,email=email,password=password1)
            user.save()
            user = authenticate(username = uname , password = password1)
            login(request, user)
            return redirect("SaveProfilePic")
        else:
            return render(request, 'users/register.html', {'error' : 'hai'})
    return render(request, 'users/register.html', {'error' : '-'})

def LoginView(request):
    if(request.user.is_authenticated):
        return render(request, 'main/home.html')
    if request.method == "POST":
        uname = request.POST.get('username')
        password = request.POST.get('password')
        if(uname != "" and password != ""):
            user = authenticate(username = uname, password = password)
            if(user != None):
                login(request, user)
                return redirect('HomeView')
        else:
            return render(request, 'users/login.html', {'msg' : 'Something wrong'})
    return render(request, 'users/login.html', {'msg' : ''})

@login_required(login_url = '')
def LogoutView(request):
    logout(request)
    return redirect('RegisterView')

def SaveProfilePic(request):
    if (request.method == 'POST' and request.is_ajax()):
        
        print(request.FILES)
        myfile = request.FILES['data']
        fr = FileSystemStorage()
        filename = fr.save(myfile.name, myfile)
        url = fr.url(filename)
        a = Users.objects.get(username = request.user.username)
        a.profilepic = url
        a.save()
        return JsonResponse({'error': False})          # return JsonResponse({'error': True})
        
    elif(request.method == "POST"):
        
        first = request.POST.get('first')
        last = request.POST.get('last')
        user = User.objects.get(username = request.user.username)
        user.first_name = first
        user.last_name = last
        user.save()
        return redirect("HomeView")
    return render(request, 'users/extrapersonal.html')


