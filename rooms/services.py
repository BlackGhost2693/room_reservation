from rest_framework.exceptions import NotAcceptable
from .models import Reservation


def reservation_checker(c_in, c_out, room):
    """
    Checks given check-in and check-out date coverage with exist reservations
    """
    reservation = Reservation.objects.filter(room=room).find_reservations(c_in, c_out)
    if reservation.exists():
        raise NotAcceptable(
            {"exist reservations": list(reservation.values('room', 'check_in', 'check_out'))})
