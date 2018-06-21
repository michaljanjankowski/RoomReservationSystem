from django.db import models

class Room(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=120
    )
    capacity = models.IntegerField()
    proj_avail = models.BooleanField()

class Reservation(models.Model):
    data = models.DateField()
    comment = models.CharField(max_length=500)
    room_id = models.ForeignKey(Room, related_name="reservation", null=True, on_delete=models.CASCADE)
    #tutaj uwaga bo w Jeden do Wiele musi być dopisana funkcja on_delete
    #natomiast jak jest Wiele do Wiele to tego robić nie trzeba, ponieważ pola nie są wówczas bezpośrednio powiązane


# Create your models here.
