from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Airline(models.Model):
    name = models.CharField(max_length=100)

    code = models.CharField(
        max_length=10,
        unique=True
    )

    country = models.CharField(max_length=100)

    logo = models.ImageField(
        upload_to="airlines/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Airport(models.Model):
    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=10,
        unique=True
    )

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city"]

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):

    FLIGHT_CLASSES = [
        ("economy", "Economy"),
        ("premium", "Premium Economy"),
        ("business", "Business"),
        ("first", "First Class"),
    ]

    STATUS = [
        ("scheduled", "Scheduled"),
        ("boarding", "Boarding"),
        ("departed", "Departed"),
        ("landed", "Landed"),
        ("cancelled", "Cancelled"),
    ]

    airline = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE,
        related_name="flights"
    )

    flight_number = models.CharField(
        max_length=20,
        unique=True
    )

    source_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures"
    )

    destination_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals"
    )

    departure_time = models.DateTimeField()

    arrival_time = models.DateTimeField()

    duration = models.DurationField()

    flight_class = models.CharField(
        max_length=20,
        choices=FLIGHT_CLASSES,
        default="economy"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_seats = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="scheduled"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return self.flight_number
    
    
class FlightBooking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="flight_bookings"
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    passengers = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"FB-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.flight.flight_number}"
