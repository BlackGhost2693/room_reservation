from datetime import datetime, timedelta
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from .models import Room, Reservation
from .serializers import ReservationSerializer, TimestampRangeSerializer


class ReservationAPIView(CreateAPIView):
    """
    API view class to reserve single or multiple rooms
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        data_set = list()
        validated_data = serializer.validated_data
        if not isinstance(validated_data, list):
            validated_data = [validated_data]
        for data in validated_data:
            from_date = data["from_date"]
            to_date = data["to_date"]
            room = data["room"]
            reservationist = data["reservationist"]
            phone = data["phone"]
            days = set([0]+list(range((to_date-from_date).days)))
            date_range = [from_date+timedelta(days=x) for x in days]
            data_set.extend([
                Reservation(
                    room=room,
                    reservationist=reservationist,
                    phone=phone,
                    date=date
                ) for date in date_range
            ])
        reservations = Reservation._default_manager.bulk_create(data_set)
        return reservations

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": "Done."}, status=status.HTTP_201_CREATED, headers=headers)


class AvailableReservationViewSet(ReadOnlyModelViewSet):
    """
    ViewSet class for available reservations
    default time range: next 7 days
    exp:
    /room/available/?room=1&from_ts=1683158400&to_ts=1683244800
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_params(self):
        """
        to manage query params
        """
        serializer = TimestampRangeSerializer(data=self.request.query_params)
        if serializer.is_valid():
            from_ts = serializer.validated_data['from_ts']
            to_ts = serializer.validated_data['to_ts']
        else:
            from_ts = serializer.default_values['from_ts']
            to_ts = serializer.default_values['to_ts']
        from_date = datetime.fromtimestamp(int(from_ts)).date()
        to_date = datetime.fromtimestamp(int(to_ts)).date()
        return from_date, to_date

    def retrieve(self, request, *args, **kwargs):
        room_pk = self.kwargs["pk"]
        try:
            Room.objects.get(id=room_pk)
        except:
            raise Http404
        exist_reservations = list(
            Reservation.objects.filter(room=room_pk)
            .find_reservations(self.get_params()[0], self.get_params()[1])
            .values("room", "date")
        )
        response = self.available_reservations([int(room_pk)], exist_reservations) 
        return Response(response)

    def list(self, request, *args, **kwargs):
        exist_reservations = list(
            Reservation.objects.find_reservations(self.get_params()[0], self.get_params()[1])
            .values("room", "date")
        )
        rooms = [room['id'] for room in Room.objects.values("id")]
        response = self.available_reservations(rooms, exist_reservations)
        return Response(response)

    def available_reservations(self, rooms, exist_reservations):
        """
        return available reservations for a period of time
        """
        _available_reservations = list()
        from_date = self.get_params()[0]
        to_date = self.get_params()[1]
        days = set([0]+list(range((to_date-from_date).days)))
        for room in rooms:
            for day in days:
                _date = from_date+timedelta(day)
                if not list(filter(lambda reservation:
                                   reservation["room"] == room and reservation["date"] == _date,
                                   exist_reservations)):
                    _available_reservations.append(
                        {"room": room, "date": _date})
        return _available_reservations
