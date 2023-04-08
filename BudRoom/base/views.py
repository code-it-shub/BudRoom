from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


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
