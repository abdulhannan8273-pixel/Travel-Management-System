from django.db import models
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.ForeignKey('destinations.Destination', on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    upadte_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Booking by {self.user} to {self.destination} on {self.booking_date}"