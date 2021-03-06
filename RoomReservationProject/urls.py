"""RoomReservationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppRoomReservation.views import View_room, modifyRoom, deleteRoom, showRoomDetails, showAllRooms, make_reservation, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new/', View_room.as_view(), name='add_room'),
    path('room/modify/<room_id>',modifyRoom, name='modify_room'),
    path('room/delete/<room_id>',deleteRoom, name='delete_room'),
    path('room/<room_id>',showRoomDetails, name='show_room_details'),
    path('/', showAllRooms, name='show_all_rooms' ),
    path('reservation/<room_id>',make_reservation, name='make_reservation'),
    path('search/', search, name='search')
]
