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
    #reservations = Reservation.objects.get(room_id=room_id) <- this way I will get an object, get gets only one object
    reservations = Reservation.objects.all().filter(room_id=room_id) #<- this way I will get QuerySet
    return render(request, 'ShowRoomDetails.html', {
        'room': room,
        'current_date': datetime.date.today(),
        'reservations':reservations
    })

def showAllRooms(request):
    allRooms = Room.objects.all()
    allTodayReservations = Reservation.objects.filter(data=datetime.date.today())
    busy_room_list =[]
    for elem in allTodayReservations:
        busy_room_list.append(elem.room_id.name)
    return render(request, 'ShowAllRooms.html', {
        'allRooms': allRooms,
        'current_date': datetime.date.today(),
        'today_reservations': busy_room_list
    })

def make_reservation(request, room_id):
    reservations = Reservation.objects.all().filter(room_id=room_id)
    reservations_list = []
    for reservation in reservations:
        reservations_list.append(reservation.data)
    #print(reservations_list)
    if request.method == 'POST':
        reservation_date = request.POST.get('reservation_date')
        reservation_date = datetime.datetime.strptime(reservation_date, '%Y-%m-%d') #it makes conversion to datetime.datetime
        reservation_date = reservation_date.date() #here it makes conversion to datetime.date
        #print(reservation_date)
        #print(type(reservation_date))
        for oldreservation in reservations_list:
            if oldreservation == reservation_date:
                didnt_add = "Room is already reserved for this day"
                return HttpResponse(didnt_add)


        if reservation_date >= datetime.date.today():
            reservation_comment = request.POST.get('reservation_comment')
            reservation=Reservation()
            reservation.comment=reservation_comment
            reservation.data=reservation_date
            reservation.room_id=Room.objects.get(id=room_id)
            reservation.save()
            return redirect('show_all_rooms')
        else:
            didnt_add ="You can to reserve room from the past"
            return HttpResponse(didnt_add)

# Create your views here.
