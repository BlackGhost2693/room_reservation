from datetime import date
from rest_framework import serializers
from .models import Room, Reservation
from .validators import phone_validator
from .services import reservation_checker


class ReservationSerializer(serializers.ModelSerializer):
    """
    serializer class for reservations
    """
    phone = serializers.CharField(validators=[phone_validator])

    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        room = attrs.get("room")
        if not date.today() <= check_in <= check_out:
            raise serializers.ValidationError("Invalid range of date for reservation.")
        reservation_checker(check_in, check_out, room)
        return super().validate(attrs)

    class Meta:
        model = Reservation
        fields = [
            "check_in",
            "check_out",
            "room",
            "reservationist",
            "phone"
        ]
