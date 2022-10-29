from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from .models import Groups, GroupChats, GroupUsers, ImageUploadGroup
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from itertools import chain
from users.models import Users

import re
# Create your views here.
@login_required
def GroupCreate(request, groupname):
    x = re.findall("[A-Za-z0-9]", groupname)
    p = ''
    x = p.join(x)  
    grouplist = request.user.creator.filter(groupname = x)
    if(len(grouplist) == 0):
        participants = request.session['groupParticipants']
        url = request.session['url']
        a = Groups.objects.create(actual = groupname, admin = request.user, groupname = x, num = len(participants), participants = str(participants), groupic = url)
        for user in participants:
            GroupUsers.objects.create(group = a, user = User.objects.get(username = user))
        return redirect('GroupView', groupname)
    else:
        return HttpResponse("Already exists")
def GroupView(request, groupname):
    x = re.findall("[A-Za-z0-9]", groupname)
    p = ''
    x = p.join(x)  
    group = Groups.objects.get(groupname = x)
    pic = group.groupic
    if request.method == 'POST':
        try:
            print(request.FILES)
            myfile = request.FILES['data']
            fr = FileSystemStorage()
            filename = fr.save(myfile.name, myfile)
            url = fr.url(filename)
            print()
            ImageUploadGroup.objects.create(path_image = url, filename = filename, chatconnect = group, sender = request.user)
            print('Imageuploaded')
            return JsonResponse({'error': False, 'path': url})
        except:
            return JsonResponse({'error': True})
    chats = group.chats.all()
    images = group.sentimages.all()
    total_msgs = list(chain(chats, images))
    total_msgs = sorted(total_msgs, key=lambda obj: obj.time)
    return render(request, 'groups/groupview.html', {'actual' : groupname, 'groupname' : x, 'user' : request.user.username, 'chats' : total_msgs, 'len' : len(total_msgs), 'pic' : pic})

@login_required
def Participants(request, name):
    group = Groups.objects.get(groupname = name)
    lst = group.groupusers.all()
    participants = []
    for i in lst:
        username = i.user.username
        user = Users.objects.get(username = username)
        participants.append([username, user.about, user.profilepic])
    participants = json.dumps(participants) 
    return render(request, 'groups/grouparticipants.html', {'participants' : participants})

@login_required
def GroupInfo(request, name):
    x = re.findall("[A-Za-z0-9]", name)
    p = ''
    x = p.join(x)  
    group = Groups.objects.get(groupname = x)
    pic = group.groupic
    return render(request, 'groups/groupinfo.html', {'username' : group.admin.username, 'numparticipants' : group.num, 'about' : group.description, 'name' : name, 'img' : pic})

    
