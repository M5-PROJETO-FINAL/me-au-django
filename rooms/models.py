from django.db import models
import uuid


class RoomType(models.Model):
    title = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=150)
    image = models.CharField(max_length=250)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"RoomType [{self.id}] - {self.title}"


class Room(models.Model):
    room_type = models.ForeignKey("rooms.RoomType", on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Room [{self.id}]"
