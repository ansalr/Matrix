from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from base.models import Room,Topic,Message
from base.forms import Roomform, Userform
# Create your views here.



# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Lets learn java!'},
#     {'id':3, 'name':'Lets learn C++!'}
# ]


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    total_room = Room.objects.all().count()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_message, 'topics':topics, 'total_room':total_room}
    return render(request, 'base/profile.html', context)
def loginuser(request):
    
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user not found')
        
        user =authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid credential')
    context = {'page':page}
    return render(request, 'base/login.html', context)


def registeruser(request):
    
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials ')

            
    context = {'form':form}
    return render(request, 'base/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')
    


    

def home(request):
        
    if request.GET.get('q') == None:
        rooms = Room.objects.all()
        room_messages = Message.objects.all()
        
    else:
        q = request.GET.get('q')
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
        
        rooms = Room.objects.filter(Q(topic__name__icontains=q)|
                                    Q(host__username__icontains=q)|
                                    Q(name__icontains=q))
        
        # rooms = Room.objects.filter(topic__name=q)
    topics = Topic.objects.all()[0:5]
    total_room = Room.objects.all().count()
    
    context = {'rooms':rooms, 'topics':topics,'total_room':total_room , 'room_messages':room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method =='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('your are not allowed')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def createroom(request):
    form = Roomform()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/form.html', context)


@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('your are not allowed')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'room':room, }
    return render(request, 'base/form.html', context)


@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('your are not allowed')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = Userform(instance=user)

    if request.method == 'POST':
        form = Userform(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form':form}
    return render(request, 'base/update_user.html', context)


def topic(request):
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(request, 'base/topic.html', context)

def activity(request):
    
    room_messages = Message.objects.all()[0:4]
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)