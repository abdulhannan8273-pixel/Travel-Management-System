from decimal import Decimal
from django.db import models
import uuid


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("upi", "UPI"),
        ("card", "Card"),
        ("net_banking", "Net Banking"),
        ("wallet", "Wallet"),
        ("cash", "Cash"),
    ]

    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="payments"
    )

    destination_booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment"
    )

    flight_booking = models.OneToOneField(
        "flights.FlightBooking",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payment"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="pending"
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id