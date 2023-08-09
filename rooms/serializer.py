from rest_framework import serializers
from .models import Room
from .models import ReservedRoom
import datetime
import pytz
from utils.exception import ValidationExecption


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ("created_at", "updated_at")
