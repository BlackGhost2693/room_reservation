from collections import OrderedDict
from datetime import timedelta, date, datetime
from rest_framework.exceptions import NotAcceptable
from .models import Reservation, Room
from .serializers import ReservationSerializer


def exist_reservations(from_date: date, to_date: date, room_id=None) -> list:
    """
    return exist reservations for a given date time range
    """
    if room_id:
        queryset = Reservation.objects.filter(room_id=room_id)\
            .find_reservations(from_date, to_date)
    else:
        queryset = Reservation.objects.find_reservations(from_date, to_date)
    _exist_reservations = ReservationSerializer(queryset, many=True).data
    return _exist_reservations


def available_reservations(from_date: date, to_date: date, room_id=None) -> list:
    """
    return available reservations for a given date time range
    """
    _available_reservations = list()
    _exist_reservations = exist_reservations(from_date, to_date, room_id)
    days = set([0]+list(range((to_date-from_date).days)))
    if room_id:
        rooms = [int(room_id)]
    else:
        rooms = [room['id'] for room in Room.objects.values("id")]
    for _room in rooms:
        for day in days:
            _date = (from_date+timedelta(day)).strftime('%Y-%m-%d')
            reservation = OrderedDict([('date', _date), ('room', _room)])
            if reservation not in _exist_reservations:
                _available_reservations.append(reservation)
    return _available_reservations


def reservation_checker(data, many):
    """
    Checks given data has coverage with exist reservations
    """
    if not many:
        data = [data]
    under_check_reservations = [
        OrderedDict(
            [
                ('date', reservation["date"]),
                ('room', int(reservation["room"]))
            ]
        ) for reservation in data
    ]
    from_date = datetime.strptime(
        min(under_check_reservations, key=lambda x: x['date'])['date'], '%Y-%m-%d').date()
    to_date = datetime.strptime(
        max(under_check_reservations, key=lambda x: x['date'])['date'], '%Y-%m-%d').date()
    _exist_reservations = exist_reservations(from_date, to_date)
    same_reservations = list()
    for reservation in under_check_reservations:
        if reservation in _exist_reservations:
            same_reservations.append(reservation)
    if same_reservations:
        raise NotAcceptable(
            {"exist_reservations": same_reservations})
