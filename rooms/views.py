from datetime import datetime
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from .models import Room, Reservation
from .serializers import ReservationSerializer, MakeReservationSerializer, TimestampRangeSerializer
from .services import available_reservations, reservation_checker


class ReservationAPIView(CreateAPIView):
    """
    API view class to reserve single or multiple rooms
    """
    queryset = Reservation.objects.all()
    serializer_class = MakeReservationSerializer

    def perform_create(self, serializer):
        data_set = list()
        validated_data = serializer.validated_data
        if not isinstance(validated_data, list):
            validated_data = [validated_data]
        for data in validated_data:
            date = data["date"]
            room_id = data["room"]
            reservationist = data["reservationist"]
            phone = data["phone"]
            data_set.append(
                Reservation(
                    room_id=room_id,
                    reservationist=reservationist,
                    phone=phone,
                    date=date
                )
            )
        reservations = Reservation._default_manager.bulk_create(data_set)
        return reservations

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        reservation_checker(serializer.initial_data, many)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": "Done."}, status=status.HTTP_201_CREATED, headers=headers)


class AvailableReservationViewSet(ReadOnlyModelViewSet):
    """
    ViewSet class for available reservations
    default time range: next 7 days
    exp:
    /room/available/2/?from_ts=1683158400&to_ts=1683244800
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
        response = available_reservations(
            self.get_params()[0],
            self.get_params()[1],
            room_pk)
        return Response(response)

    def list(self, request, *args, **kwargs):
        response = available_reservations(
            self.get_params()[0],
            self.get_params()[1],
        )
        return Response(response)
