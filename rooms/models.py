from django.db import models
from core.base_model import RootModel


class Room(RootModel):
    """
    model class for rooms
    """
    ROOM_TYPE = (
        ("Single", "Single"),
        ("Double", "Double"),
        ("Triple", "Triple"),
        ("Quad", "Quad"),
        ("VIP", "VIP")
    )
    type = models.CharField(choices=ROOM_TYPE, max_length=6)
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)


class Reservation(RootModel):
    """
    model class for users reservations
    """
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservationist = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.room}|{self.reservationist}"


