from django.db import models
from django.conf import settings


class SearchLog(models.Model):
    """One row per search performed through GET /api/search/?q=... .
    Used only to compute 'popular searches' — not shown to end users directly."""

    query = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="search_logs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "search_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.query