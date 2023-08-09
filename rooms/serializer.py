from rest_framework import serializers
from .models import Room
from utils.exception import ValidationException


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("created_at", "updated_at")
