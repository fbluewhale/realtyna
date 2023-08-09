from django.db import models
from rooms.models import Room
from utils.models import BaseModel


class ReservedRoom(BaseModel):
    date = models.DateField()
    room = models.ForeignKey(
        Room, related_name="reserved_room", on_delete=models.PROTECT
    )
    owner = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.room.title}-{self.room.number}-{self.date}--{self.owner}"
