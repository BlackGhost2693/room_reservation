from datetime import datetime, timedelta
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer, TimestampRangeSerializer


class ReservationAPIView(CreateAPIView):
    """
    API view class to reserve single or multiple rooms
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": "Done."}, status=status.HTTP_201_CREATED, headers=headers)


class AvailableReservationAPIView(ListAPIView):
    """
    API view class for available reservations
    default time range: next 7 days
    exp:
    /room/available/?room=1&from_ts=1683158400&to_ts=1683244800
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    from_date = None
    to_date = None

    def get_queryset(self):
        serializer = TimestampRangeSerializer(data=self.request.query_params)
        if serializer.is_valid():
            from_ts = serializer.validated_data['from_ts']
            to_ts = serializer.validated_data['to_ts']
        else:
            from_ts = serializer.default_values['from_ts']
            to_ts = serializer.default_values['to_ts']
        self.from_date = datetime.fromtimestamp(int(from_ts)).date()
        self.to_date = datetime.fromtimestamp(int(to_ts)).date()
        room = self.request.query_params.get('room')
        if room:
            try:
                return super().get_queryset().filter(room=room).find_reservations(self.from_date, self.to_date)
            except:
                raise Http404
        return super().get_queryset().find_reservations(self.from_date, self.to_date)

    def list(self, request, *args, **kwargs):
        exist_reservations = self.filter_queryset(self.get_queryset())
        rooms = exist_reservations.values("room").distinct()
        days = set([0]+list(range((self.to_date-self.from_date).days)))
        available_reservations = list()
        for room in rooms:
            for day in days:
                _room = room['room']
                _date = self.from_date+timedelta(day)
                if not exist_reservations.filter(room=_room, date=_date).exists():
                    available_reservations.append(
                        {"room": _room, "date": _date})
        return Response(available_reservations)
