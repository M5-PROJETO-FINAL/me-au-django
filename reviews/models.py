from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Reviews(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    review_text = models.CharField(max_length=255)
    stars = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    reservation = models.ManyToManyField('reservations.Reservation', related_name="reviews")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reviews")