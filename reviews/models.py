from django.db import models

class Reviews(models.Model):
    class Meta: 
        ordering = ["id"]

    review_text = models.CharField(max_length=255)
    stars = models.PositiveIntegerField(max_value=5)
    reservation = models.ManyToManyField('reservations.Reservation', on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reviews")