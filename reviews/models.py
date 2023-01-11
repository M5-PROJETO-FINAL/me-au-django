from django.db import models
import uuid


class Reviews(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    review_text = models.TextField()
    stars = models.PositiveIntegerField()
    reservation = models.OneToOneField(
        "reservations.Reservation", on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
