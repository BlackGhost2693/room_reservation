import time
from datetime import date
from rest_framework import serializers
from .models import Reservation
from .validators import phone_validator
from .services import reservation_checker


class ReservationSerializer(serializers.ModelSerializer):
    """
    serializer class to make reservations
    """
    from_date = serializers.DateField(write_only=True)
    to_date = serializers.DateField(write_only=True)
    phone = serializers.CharField(validators=[phone_validator])

    def validate(self, attrs):
        from_date = attrs.get("from_date")
        to_date = attrs.get("to_date")
        room = attrs.get("room")
        if not date.today() <= from_date <= to_date:
            raise serializers.ValidationError(
                "Invalid range of date for reservation.")
        reservation_checker(from_date, to_date, room)
        return super().validate(attrs)

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    class Meta:
        model = Reservation
        fields = [
            "from_date",
            "to_date",
            "room",
            "reservationist",
            "phone"
        ]


class TimestampRangeSerializer(serializers.Serializer):
    """
    serializer class for timestamps given from endpoint /rooms/available
    """
    current_ts = int(time.time())
    week_ts = current_ts + 7*24*3600
    from_ts = serializers.CharField()
    to_ts = serializers.CharField()

    def validate(self, attrs):
        from_ts = attrs.get("from_ts")
        to_ts = attrs.get("to_ts")
        if not from_ts.isdigit() or not to_ts.isdigit():
            raise serializers.ValidationError("Invalid timestamp.")
        if not self.current_ts <= int(from_ts) <= int(to_ts) <= self.week_ts:
            raise serializers.ValidationError("Invalid time range.")
        return super().validate(attrs)

    @property
    def default_values(self):
        return {
            "from_ts": self.current_ts,
            "to_ts": self.week_ts
        }