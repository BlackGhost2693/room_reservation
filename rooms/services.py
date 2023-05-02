from django.db.models import Q
from rest_framework.exceptions import NotAcceptable
from .models import Reservation


def reservation_checker(check_in, check_out, room):
    """
    Checks given check-in and check-out date coverage with exist reservations
    """
    cond1 = Q(check_in__range=[check_in, check_out])
    cond2 = Q(check_out__range=[check_in, check_out])
    cond3 = Q(check_in__lte=check_in, check_out__gte=check_out)
    reservation = Reservation.objects.filter(
        room=room).filter(cond1 | cond2 | cond3)
    if reservation.exists():
        raise NotAcceptable(
            'A reservation with this date range already exists.')
