import pytz
import datetime
from rest_framework import serializers
from .models import ReservedRoom
from utils.exception import ValidationException


class ReservedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedRoom
        exclude = ("id", "created_at", "updated_at","booking_date")


class AvailableRoomSerializer(serializers.Serializer):
    checking_date = serializers.DateTimeField(required=True, input_formats=["%Y-%m-%d"])
    checkout_date = serializers.DateTimeField(required=True, input_formats=["%Y-%m-%d"])

    def validate_date(self, value):
        if value >= datetime.datetime.now().replace(tzinfo=pytz.UTC):
            raise ValidationException("")
        return value

    def validate(self, data):
        if data.get("checkout_date") < data.get("checking_date"):
            raise ValidationException("checkout date most be grater than checking date")
        return data

class CheckRoomIsAvailableSerializer(serializers.Serializer):
    checking_date = serializers.DateTimeField(required=True, input_formats=["%Y-%m-%d"])
    checkout_date = serializers.DateTimeField(required=True, input_formats=["%Y-%m-%d"])
    room = serializers.UUIDField()


class BookRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedRoom
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class BookedRoomReportQuerySerializer(serializers.Serializer):
    start_date = serializers.DateTimeField(input_formats=["%Y-%m-%d"])
    end_date = serializers.DateTimeField(input_formats=["%Y-%m-%d"])
    room =  serializers.UUIDField(required=False)
    # def validate_start_date(self, value):
    #     if value >= datetime.datetime.now().replace(tzinfo=pytz.UTC):
    #         raise ValidationException("")
    #     return value

    def validate(self, data):
        if data.get("end_date") < data.get("start_date"):
            raise ValidationException("end date most be grater than start date")
        return data
