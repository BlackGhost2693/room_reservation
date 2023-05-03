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

    def find_reservations(self, from_date, to_date):
        """
        find reservations for a given period of time 
        """
        return self.filter(date__range=[from_date, to_date])


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
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservationist = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)

    objects = ReservationManager()

    def __str__(self):
        return f"room {self.room_id}| reserved date {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'room'], name='unique_date_room')
        ]


