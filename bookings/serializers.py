from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Cat't book in the past!")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Cat't book in the past!")
        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError("Check in should be before check out")
        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some of) dates are already taken."
            )
        return data


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience_time = serializers.DateTimeField()
    experience_duration = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "experience_duration",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Cat't book in the past!")
        return value

    def validate_experience_duration(self, value):
        if value < 1:
            raise serializers.ValidationError("Duration should be greater than 0")
        if value > 24:
            raise serializers.ValidationError("Duration should be less than 24")
        return value

    def validate(self, data):
        if Booking.objects.filter(
            experience_time__lte=data["experience_time"]
            + timezone.timedelta(hours=data["experience_duration"]),
            experience_time__gte=data["experience_time"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some of) dates are already taken."
            )
        return data


class PublicRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience_time",
            "experience_duration",
            "guests",
        )
