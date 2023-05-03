from datetime import date, timedelta
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

    def create(self, validated_data):
        return super().create(validated_data)

    def create(self, validated_data):
        from_date = validated_data["from_date"]
        to_date = validated_data["to_date"]
        room = validated_data["room"]
        reservationist = validated_data["reservationist"]
        phone = validated_data["phone"]
        days = set([0]+list(range((to_date-from_date).days)))
        date_range = [from_date+timedelta(days=x) for x in days]
        ModelClass = self.Meta.model
        reservations = ModelClass._default_manager.bulk_create([
            ModelClass(
                room=room,
                reservationist=reservationist,
                phone=phone,
                date=date
            ) for date in date_range
        ])
        return reservations[0]

    class Meta:
        model = Reservation
        fields = [
            "from_date",
            "to_date",
            "room",
            "reservationist",
            "phone"
        ]
