from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Exactly one of these three should be set — enforced in the serializer,
    # since a plain unique_together doesn't work cleanly with nullable FKs.
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews"
    )
    package = models.ForeignKey(
        "packages.Package",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews"
    )
    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        target = self.destination or self.package or self.hotel
        return f"{self.user.email} - {target}"