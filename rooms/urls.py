from django.urls import path, include
from rest_framework import routers
from .views import ReservationAPIView, AvailableReservationViewSet


router = routers.DefaultRouter()
router.register(r'', AvailableReservationViewSet)


urlpatterns = [
    path("reserve/", ReservationAPIView.as_view()),
    path("available/", include(router.urls))
]