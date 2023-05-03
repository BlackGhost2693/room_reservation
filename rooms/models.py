from django.db.models import Q
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

    def __str__(self):
        return str(self.id)


class ReservationQuerySet(models.query.QuerySet):
    """
    custom QuerySet for Reservation model
    """

    def find_reservations(self, c_in, c_out):
        """
        find reservations for a given period of time 
        """
        cond1 = Q(check_in__range=[c_in, c_out])
        cond2 = Q(check_out__range=[c_in, c_out])
        cond3 = Q(check_in__lte=c_in, check_out__gte=c_out)
        return self.filter(cond1 | cond2 | cond3)


class ReservationManager(models.manager.BaseManager.from_queryset(ReservationQuerySet)):
    """
    custom manager for Reservation model
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Reservation(RootModel):
    """
    model class for users reservations
    """
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservationist = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    objects = ReservationManager()

    def __str__(self):
        return f"room {self.room}| reserved dates {self.check_in}-{self.check_out}"


