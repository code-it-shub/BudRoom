from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


# Create your views here.
# rooms =[
#     {'id' :1, 'name':'lets learn python!'},
#     {'id' :2, 'name':'lets learn javascript!'},
#     {'id' :3, 'name':'lets learn php!'},

# ]
def home(request):
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request,'base/home.html',context)

def room(request,pk):
    # room = None
    rooms = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id']== int(pk):
    #         room = i
    params = {'room':rooms}
    return render(request,'base/room.html',params)

def createroom(request):
    form = RoomForm()
    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('home') 
    context={'form' : form}
    return render (request,'base/room_form.html',context)


def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()  
            return redirect('home')
    
    context ={'form' : form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context ={'obj' : room}
    return render(request,'base/deleteRoom.html', context)
        

