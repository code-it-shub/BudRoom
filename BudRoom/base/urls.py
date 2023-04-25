from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logoutUser"),
    path('register/',views.registerUser,name="registerUser"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('room_form/',views.createroom,name="createroom"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('deleteRoom/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('deleteMessage/<str:pk>/',views.deleteMessage,name="delete-message")
]