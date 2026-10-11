from django.db import models


class Report(models.Model):
    REPORT_TYPES = [
        ("booking", "Booking"),
        ("payment", "Payment"),
        ("user", "User"),
        ("hotel", "Hotel"),
        ("flight", "Flight"),
    ]

    title = models.CharField(max_length=200)

    report_type = models.CharField(
        max_length=20,
        choices=REPORT_TYPES
    )

    description = models.TextField(blank=True)

    generated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="reports"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title