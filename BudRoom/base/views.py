from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Topic, Message
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm,Userform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# rooms =[
#     {'id' :1, 'name':'lets learn python!'},
#     {'id' :2, 'name':'lets learn javascript!'},
#     {'id' :3, 'name':'lets learn php!'},
# ]

def loginPage(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('Username').lower()
        password = request.POST.get('Password')

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
            
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR password does not exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerUser(request):
    page = registerUser
    form = UserCreationForm()
    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An Error occured during registration ')

    context = {'page' : page,
               'form': form}
    return render(request,'base/login_register.html',context)


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_msgs =user.message_set.all()
    room_participated=Room.objects.filter(participants=user)
    topics=Topic.objects.all()
    context={'user':user, 'rooms': rooms ,'room_msgs':room_msgs, 'topics' : topics , 'room_participated':room_participated}
    return render(request,'base/profile.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    # if q==None:
    #     rooms=Room.objects.all()
    # else:
    #     rooms = Room.objects.filter(topic__name=q)
    room_count=rooms.count()
    topics = Topic.objects.all()
    room_msgs= Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics,'roomCount' : room_count, 'room_msgs': room_msgs}
    return render(request, 'base/home.html', context)


def room(request, pk):
    # room = None
    room = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id']== int(pk):
    #         room = i
    room_msgs= room.message_set.all().order_by('created')  # message_set is Message class in model 
    if request.method == 'POST':
        if request.user.is_authenticated:
            message=Message.objects.create(
                user= request.user,
                room=room,
                body= request.POST.get('msg')
            )
            currUser= request.user
            room.participants.add( currUser)
            return redirect('room', pk=room.id)
        else:
            return redirect('login')
    participants= room.participants.all()  
    topics = Topic.objects.all()
    params = {'room': room , 'room_msgs': room_msgs, 'participants':participants, 'topics' :topics}
    return render(request, 'base/room.html', params)

@login_required(login_url='/login')
def createroom(request):
    form = RoomForm()
    topics= Topic.objects.all() 
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            topic=topic,
            # participants=request.user,
            host=request.user,
            name=request.POST.get('room_name'),
            description = request.POST.get('description')
        )
        Room.save()
        return redirect('home')
        
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host =request.user
        #     room.save()
        #     return redirect('home')
    context = {'form': form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not allowed to do modifications")
    else:
        if request.method == 'POST':
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form': form}
        return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to do modifications")
    else:
        if request.method == 'POST':
            room.delete()
            return redirect('home')
        context = {'obj': room}
        return render(request, 'base/deleteRoom.html', context)


@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to do modifications")
    else:
        if request.method == 'POST':
            message.delete()  
            return redirect('home')
        context = {'obj': message}
        return render(request, 'base/deleteRoom.html', context)

@login_required(login_url="/login")
def updateUser(request):
    form = Userform(instance=request.user)
    if request.method == 'POST':
        form = Userform(request.POST , instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=request.user.id)
    context={'form':form}
    return render(request, 'base/profile-update.html', context)

