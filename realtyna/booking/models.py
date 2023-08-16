from django.db import models
from rooms.models import Room
from utils.models import BaseModel


class ReservedRoom(BaseModel):
    # date = models.DateField()
    room = models.ForeignKey(
        Room, related_name="reserved_room", on_delete=models.PROTECT
    )
    owner = models.CharField(max_length=100)
    booking_date = models.DateField(auto_now_add=True)
    checking_date = models.DateField(blank=True, null=True)
    checkout_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.room.title}-{self.room.number}-{self.checking_date}-{self.checkout_date }-{self.owner}"
