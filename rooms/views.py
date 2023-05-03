from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer


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