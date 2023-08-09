from django.db import models
from utils.models import BaseModel


class Room(BaseModel):
    number = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, default="")

    def __str__(self) -> str:
        return f"{self.title}-{self.number}"
