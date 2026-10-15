from django.db import models


class FAQ(models.Model):
    package = models.ForeignKey(
        "packages.Package",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faqs",
        help_text="Leave blank for a general sitewide FAQ; set this to attach the FAQ to one specific package.",
    )
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "faqs"
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question