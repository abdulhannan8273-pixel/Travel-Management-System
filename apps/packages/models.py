from django.db import models

# Create your models here.
from apps.destinations.models import Destination

class Package(models.Model):
    Destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    max_persons = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to="packages/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "packages"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name