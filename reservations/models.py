import uuid
from django.db import models
from django.core.validators import MinValueValidator


class ReservationStatusChoices(models.Choices):
    RESERVED = "reserved"
    ACTIVE = "active"
    CONCLUDED = "concluded"
    CANCELLED = "cancelled"


class Reservation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    checkin = models.DateField()
    checkout = models.DateField()
    status = models.CharField(
        max_length=9,
        choices=ReservationStatusChoices.choices,
        default=ReservationStatusChoices.RESERVED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)


class ReservationService(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    service = models.ForeignKey("services.Service", on_delete=models.CASCADE)
    reservation = models.ForeignKey(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="reservation_services",
        null=True,
    )
    amount = models.IntegerField(validators=[MinValueValidator(0)])


class ReservationPet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    reservation = models.ForeignKey(
        "reservations.Reservation",
        on_delete=models.CASCADE,
        related_name="reservation_pets",
        null=True,
    )
    pet = models.ForeignKey("pets.Pet", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)
