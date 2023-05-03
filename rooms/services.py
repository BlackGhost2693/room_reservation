from rest_framework.exceptions import NotAcceptable
from .models import Reservation


def reservation_checker(from_date, to_date, room):
    """
    Checks given check-in and check-out date coverage with exist reservations
    """
    reservation = Reservation.objects.filter(room=room).find_reservations(from_date, to_date)
    if reservation.exists():
        raise NotAcceptable(
            {"exist reservations": list(reservation.values('room', 'date'))})
