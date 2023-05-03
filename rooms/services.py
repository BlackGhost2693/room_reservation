from rest_framework.exceptions import NotAcceptable
from .models import Reservation


def reservation_checker(from_date, to_date, room):
    """
    Checks given check-in and check-out date coverage with exist reservations
    """
    reservation = list(
        Reservation.objects.filter(room=room)
        .find_reservations(from_date, to_date)
        .values('room', 'date')
    )
    if reservation:
        raise NotAcceptable(
            {"exist reservations": reservation})
