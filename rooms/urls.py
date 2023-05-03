from django.urls import path
from .views import ReservationAPIView, AvailableReservationAPIView


urlpatterns = [
    path("reserve/", ReservationAPIView.as_view()),
    path("available/", AvailableReservationAPIView.as_view())
]