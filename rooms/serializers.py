import time
from django.utils.functional import cached_property
from rest_framework import serializers
from .models import Room, Reservation
from .validators import phone_validator


class ReservationSerializer(serializers.ModelSerializer):
    """
    serializer class for reservations
    """

    class Meta:
        model = Reservation
        fields = [
            "date",
            "room",
        ]


class MakeReservationSerializer(serializers.ModelSerializer):
    """
    serializer class to make reservations
    """
    room = serializers.IntegerField()
    phone = serializers.CharField(validators=[phone_validator])

    @cached_property
    def all_rooms(self):
        queryset = Room.objects.all().values("id")
        rooms = [room['id'] for room in queryset]
        return rooms

    def validate(self, attrs):
        date = attrs.get("date")
        room = attrs.get("room")
        if not date.today() <= date:
            raise serializers.ValidationError(
                "Invalid date for reservation.")
        if room not in self.all_rooms:
            raise serializers.ValidationError(
                f"Invalid room {room} - object does not exist.")
        return super().validate(attrs)

    class Meta:
        model = Reservation
        fields = [
            "date",
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