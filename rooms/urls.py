from django.urls import path
from .views import ReservationAPIView


urlpatterns = [
    path("reserve/", ReservationAPIView.as_view())
]