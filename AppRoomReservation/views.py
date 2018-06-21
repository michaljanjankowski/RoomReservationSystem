from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation, Room
import arrow
import datetime

class View_room(View):
    def get(self, request):
        return render(request, 'CreateNewRoom.html')

    def post(self, request):
        room_name = request.POST.get('name')
        room_capacity = request.POST.get('capacity')
        room_projector = request.POST.get('projector')
        if room_projector is None:
            room_projector = False
        elif room_projector =="on":
            room_projector = True

        room = Room()
        room.name = room_name
        room.capacity = room_capacity
        room.proj_avail = room_projector
        room.save()

        #dodano = "Room Added"
        #return HttpResponse(dodano)
        return redirect('show_all_rooms')


def modifyRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'GET':
        return render(request, 'ModifyRoom.html', {
            'room': room
        })
    elif request.method == 'POST':
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        proj_avail = bool(request.POST.get('projector'))
        room.name = name
        room.capacity = capacity
        room.proj_avail = proj_avail
        room.save()
        return redirect('show_all_rooms')



def deleteRoom(request, room_id):
    room_to_delete = Room.objects.get(id=room_id)
    name = room_to_delete.name
    room_to_delete.delete()
    return redirect('show_all_rooms')

def showRoomDetails(request, room_id):
    room = Room.objects.get(id=room_id)
    #reservations = Reservation.objects.get(room_id=room_id) <- this way I will get an object
    reservations = Reservation.objects.all().filter(room_id=room_id) #<- this way I will get QuerySet
    return render(request, 'ShowRoomDetails.html', {
        'room': room,
        'current_date': datetime.date.today(),
        'reservations':reservations
    })

def showAllRooms(request):
    allRooms = Room.objects.all()
    return render(request, 'ShowAllRooms.html', {
        'allRooms': allRooms, 'current_date': datetime.date.today()
    })

def make_reservation(request, room_id):
    if request.method == 'POST':
        reservation_date = request.POST.get('reservation_date')
        print(reservation_date)
        print(type(reservation_date))
        reservation_comment = request.POST.get('reservation_comment')
        print(reservation_comment)
        reservation=Reservation()
        reservation.comment=reservation_comment
        reservation.data=reservation_date
        reservation.room_id=Room.objects.get(id=room_id)
        reservation.save()
        return redirect('show_all_rooms')

# Create your views here.
